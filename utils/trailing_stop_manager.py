import json
from datetime import datetime as dt

from judas_ibkr.safe_order import safe_execute
from utils.broker_adapter import fetch_ibkr_state
from judas_reflective_intelligence.rebalance_scheduler_ai import generate_target_weights

# Phase 2 managers
from utils.profit_tracker import ProfitTracker
from utils.take_profit_manager import TakeProfitManager
from utils.dynamic_scaling_manager import DynamicScalingManager
# Phase 3 manager: Trailing Stop
from utils.trailing_stop_manager import TrailingStopManager

class Rebalancer:
    def __init__(
        self,
        watch_list: list[str],
        leverage: float,
        threshold: float,
        max_trade_fraction: float,
        min_price_points: int,
        ib,
    ):
        self.watch_list          = watch_list
        self.leverage            = leverage
        self.threshold           = threshold
        self.max_trade_fraction  = max_trade_fraction
        self.min_price_points    = min_price_points
        self.ib                  = ib
        self.prices              = {s: None for s in watch_list}
        self.last_rebalance_time = dt.utcnow()

        # Phase 2: Profit & Scaling
        self.profit_tracker      = ProfitTracker()
        self.take_profit_mgr     = TakeProfitManager(self.profit_tracker)
        self.scaler              = DynamicScalingManager(self.profit_tracker)
        # Phase 3: Trailing Stop
        self.trailing_stop_mgr   = TrailingStopManager(self.profit_tracker, drawdown_pct=3.0)

    def update_price(self, symbol: str, price: float):
        # Price feed update
        self.prices[symbol] = price
        # Phase 2: update profit tracker
        self.profit_tracker.update_price(symbol, price)
        # Phase 3: update trailing stop peak
        self.trailing_stop_mgr.update_price(symbol, price)

    def should_rebalance(self, now=None):
        now = now or dt.utcnow()
        elapsed = (now - self.last_rebalance_time).total_seconds()
        return elapsed >= self.min_price_points and all(self.prices.values())

    async def execute(self):
        # 1) fetch current state
        result = await fetch_ibkr_state(self.ib)
        if isinstance(result, tuple) and len(result) == 2:
            cash, positions = result
        else:
            cash = result
            positions = {}

        # 2) compute portfolio value
        total_value = cash + sum(self.prices[s] * positions.get(s, 0) for s in self.watch_list)

        # 3) compute target weights (AI model)
        target_weights = generate_target_weights(self.prices, total_value, positions)

        # 4) rebalance trades
        for sym, w in target_weights.items():
            desired_qty = int(w * total_value / self.prices[sym])
            current_qty = positions.get(sym, 0)
            delta = desired_qty - current_qty
            price_ref = self.prices[sym]

            side = 'BUY' if delta > 0 else 'SELL'
            size = abs(delta)
            print(f"[{dt.now()}] [safe_execute] {side} {size} {sym} @ market (ref={price_ref})")

            safe_execute(self.ib, sym, delta, price_ref, False)
            if delta > 0:
                self.profit_tracker.update_entry(sym, price_ref)

        # 5) Take-Profit checks
        for sym in self.watch_list:
            self.take_profit_mgr.check_and_execute(sym)

        # 6) Dynamic Scaling checks
        for sym in self.watch_list:
            base_qty = positions.get(sym, 0)
            if base_qty > 0:
                self.scaler.update_and_scale(sym, base_qty)

        # 7) Trailing-Stop checks
        for sym in self.watch_list:
            qty = positions.get(sym, 0)
            if qty > 0:
                self.trailing_stop_mgr.check_and_execute(sym, quantity=qty)

        self.last_rebalance_time = dt.utcnow()

    async def stream_and_rebalance(self, ps):
        msg = await ps.get_message(ignore_subscribe_messages=True, timeout=1.0)
        if msg and msg['type'] == 'message':
            payload = json.loads(msg['data'])
            print(f"[{dt.now()}] Tick → {payload['s']} @ {payload['p']}")
            self.update_price(payload['s'], payload['p'])
        if self.should_rebalance(now=dt.utcnow()):
            print(f"[{dt.now()}] → Rebalance triggered")
            await self.execute()
