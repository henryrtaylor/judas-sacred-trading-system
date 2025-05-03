#!/usr/bin/env python
import os
import sys
import logging
import asyncio
import json
import redis.asyncio as aioredis
from datetime import datetime as dt, timedelta
from functools import lru_cache
from ib_insync import IB, Stock

# Disable IB destructor to prevent "Event loop is closed" errors on script exit
IB.__del__ = lambda self: None

# ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(__file__, '..')))

# Logging setup: file and console handlers
os.makedirs('logs', exist_ok=True)
# Create formatter
formatter = logging.Formatter('[%(asctime)s] %(message)s')
# File handler
file_handler = logging.FileHandler('logs/rebalancer.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
# Configure root logger
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(file_handler)
logging.getLogger().addHandler(console_handler)
logger = logging.getLogger(__name__)

# Strategy parameters (env vars override defaults)
WATCH_LIST = os.getenv('WATCH_LIST', 'SPY,QQQ,TLT,GLD,AAPL,NVDA,AMZN').split(',')
REDIS_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379')
IB_HOST = os.getenv('IBKR_HOST', '127.0.0.1')
IB_PORT = int(os.getenv('IBKR_API_PORT', '7497'))
IB_CLIENT_ID = int(os.getenv('IBKR_CLIENT_ID', '1'))
INTERVAL = int(os.getenv('REBALANCE_INTERVAL', '60'))  # seconds
MIN_PRICE_POINTS = int(os.getenv('MIN_PRICE_POINTS', '4'))

@lru_cache(maxsize=None)
def cached_bars(symbol: str, fetched_on: int):
    from utils.data_router import get_bars
    return get_bars(
        symbol,
        start=dt.utcnow().date().isoformat(),
        end=(dt.utcnow().date() + timedelta(days=1)).isoformat(),
    )

class Rebalancer:
    def __init__(self, watch_list, min_price_points, ib):
        self.watch_list = watch_list
        self.min_price_points = min_price_points
        self.ib = ib
        self.prices = {s: None for s in watch_list}
        self.last_rebalance_time = dt.utcnow()
        # Managers
        from utils.profit_tracker import ProfitTracker
        from utils.take_profit_manager import TakeProfitManager
        from utils.dynamic_scaling_manager import DynamicScalingManager
        from utils.trailing_stop_manager import TrailingStopManager
        from utils.risk_guard_manager import RiskGuardManager
        self.profit_tracker = ProfitTracker()
        self.take_profit_mgr = TakeProfitManager(self.profit_tracker)
        self.scaler = DynamicScalingManager(self.profit_tracker)
        self.trailing_stop_mgr = TrailingStopManager(self.ib, self.profit_tracker, drawdown_pct=3.0)
        self.risk_guard = RiskGuardManager(max_drawdown_pct=5.0, max_daily_loss_pct=2.0)

    def update_price(self, symbol, price):
        logger.debug(f"Price update: {symbol} @ {price}")
        self.prices[symbol] = price
        self.profit_tracker.update_price(symbol, price)
        self.trailing_stop_mgr.update_price(symbol, price)

    def should_rebalance(self, now=None):
        now = now or dt.utcnow()
        elapsed = (now - self.last_rebalance_time).total_seconds()
        active = [s for s, p in self.prices.items() if p is not None]
        return elapsed >= self.min_price_points and len(active) >= self.min_price_points

    async def fetch_price_async(self, symbol):
        contract = Stock(symbol, 'SMART', 'USD')
        ticker = await self.ib.reqMktDataAsync(contract, '', False, False)
        for _ in range(10):
            price = getattr(ticker, 'marketPrice', None)
            if price:
                return price
            await asyncio.sleep(0.1)
        raise RuntimeError(f"Timeout fetching price for {symbol}")

    async def execute(self):
        logger.info("Rebalance begin")
        # Fallback missing prices
        for sym in self.watch_list:
            if self.prices.get(sym) is None:
                self.update_price(sym, await self.fetch_price_async(sym))
        # Account state
        from utils.broker_adapter import fetch_ibkr_state
        result = await fetch_ibkr_state(self.ib)
        cash, positions = (result if isinstance(result, tuple) else (result, {}))
        total = cash + sum(self.prices[s] * positions.get(s, 0) for s in self.watch_list)
        logger.info(f"Portfolio value={total:.2f}")
        # Risk guard
        self.risk_guard.record_portfolio_value(total)
        if self.risk_guard.enforce(self.ib, positions, total):
            self.last_rebalance_time = dt.utcnow()
            return
        # Allocation
        from judas_reflective_intelligence.rebalance_scheduler_ai import generate_target_weights
        weights = generate_target_weights(self.prices, total, positions)
        logger.info(f"Target weights={weights}")
        # Orders
        from judas_ibkr.safe_order import safe_execute
        for sym, w in weights.items():
            price = self.prices[sym]
            desired = int(w * total / price)
            current = positions.get(sym, 0)
            delta = desired - current
            side = 'BUY' if delta > 0 else 'SELL'
            qty = abs(delta)
            logger.info(f"Order: {side} {qty} {sym} @ {price}")
            try:
                safe_execute(self.ib, sym, delta, price, False)
            except Exception as e:
                logger.error(f"Order failed {sym}: {e}")
        # Cleanup
        for sym in set(positions) - set(weights):
            qty = positions[sym]
            if qty > 0:
                logger.info(f"Cleanup sell {qty} {sym}")
                try:
                    safe_execute(self.ib, sym, -qty, self.prices.get(sym, 0), False)
                except Exception:
                    pass
        # Managers: take‑profit, scaling, trailing stops (sync or async)
        import asyncio
        for sym in self.watch_list:
            # Take‑profit manager (may be sync or async)
            tp_res = self.take_profit_mgr.check_and_execute(sym)
            if asyncio.iscoroutine(tp_res):
                await tp_res

            base_qty = positions.get(sym, 0)
            if base_qty > 0:
                # Dynamic scaling manager
                ds_res = self.scaler.update_and_scale(sym, base_qty)
                if asyncio.iscoroutine(ds_res):
                    await ds_res
                # Trailing stop manager
                ts_res = self.trailing_stop_mgr.check_and_execute(sym, quantity=base_qty)
                if asyncio.iscoroutine(ts_res):
                    await ts_res
        self.last_rebalance_time = dt.utcnow()

async def main():
    # Redis
    redis = aioredis.from_url(REDIS_URL)
    ps = redis.pubsub()
    await ps.subscribe(*[f"ticks:{s}" for s in WATCH_LIST])
    # IBKR
    ib = IB()
    await ib.connectAsync(IB_HOST, IB_PORT, clientId=IB_CLIENT_ID)
    logger.info(f"IB connected={ib.isConnected()}")
    # Rebalancer
    reb = Rebalancer(WATCH_LIST, MIN_PRICE_POINTS, ib)
    # Seed prices
    from utils.redis_ticks import last_price
    for s in WATCH_LIST:
        p = await last_price(s)
        if p is not None:
            reb.update_price(s, p)
    logger.info("Starting stream...")
    try:
        while True:
            msg = await ps.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if msg and msg['type']=='message':
                data = json.loads(msg['data'])
                reb.update_price(data['s'], data['p'])
            if reb.should_rebalance():
                await reb.execute()
            await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        logger.info("Shutdown: disconnecting...")
    finally:
        if ib.isConnected():
            ib.disconnect()

if __name__=='__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
