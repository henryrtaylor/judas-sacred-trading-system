#!/usr/bin/env python
import sys, os
# ensure project root (one level above this script) is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(__file__, '..')))

import asyncio
import json
import redis.asyncio as aioredis

from datetime import datetime as dt, timedelta
from functools import lru_cache

from ib_insync import IB

# import last_price from utils
from utils.redis_ticks import last_price
from utils.data_router import get_bars
from utils.broker_adapter import fetch_ibkr_state

# ─── Strategy parameters (env vars override defaults) ───────────────────────────
WATCH_LIST = os.getenv('WATCH_LIST', "SPY,QQQ,TLT,GLD,AAPL,NVDA,AMZN").split(',')
REDIS_URL           = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379')
IB_HOST             = os.getenv('IBKR_HOST', '127.0.0.1')
IB_PORT             = int(os.getenv('IBKR_API_PORT', 7497))
IB_CLIENT_ID        = int(os.getenv('IBKR_CLIENT_ID', 1))
INTERVAL = int(os.getenv('REBALANCE_INTERVAL', '60'))      # seconds between rebalances
LEVERAGE            = float(os.getenv('PORTFOLIO_LEVERAGE', 1.0))
MIN_PRICE_POINTS    = int(os.getenv('MIN_PRICE_POINTS', 4))         # bars for fallback
THRESHOLD = float(os.getenv('REBALANCE_THRESHOLD', '0.05'))  # fraction of equity
MAX_TRADE_FRACTION = float(os.getenv('REBALANCE_MAX_TRADE', '0.1'))   # fraction of equity per trade
# ────────────────────────────────────────────────────────────────────────────────

@lru_cache(maxsize=None)
def cached_bars(symbol: str, fetched_on: int):
    return get_bars(
        symbol,
        start=dt.utcnow().date().isoformat(),
        end=(dt.utcnow().date() + timedelta(days=1)).isoformat(),
    )

async def stream_and_rebalance():
    # 1) connect to Redis pub/sub
    redis = aioredis.from_url(REDIS_URL)
    ps = redis.pubsub()
    await ps.subscribe(*[f"ticks:{s}" for s in WATCH_LIST])
    print(f"[Rebalancer] Subscribed to channels: {[f'ticks:{s}' for s in WATCH_LIST]}")

    # 2) connect to IBKR asynchronously
    ib = IB()
    await ib.connectAsync(IB_HOST, IB_PORT, clientId=IB_CLIENT_ID)

    # 3) instantiate your Rebalancer
    from judas_ibkr.rebalancer import Rebalancer
    rebalancer = Rebalancer(
        watch_list=WATCH_LIST,
        leverage=LEVERAGE,
        threshold=THRESHOLD,
        max_trade_fraction=MAX_TRADE_FRACTION,
        min_price_points=MIN_PRICE_POINTS,
        ib=ib
    )

    # 4) seed with last known prices
    for s in WATCH_LIST:
        price = await last_price(s)
        if price is not None:
            rebalancer.update_price(s, price)

    last_rebalance = dt.utcnow()
    print(f"[{dt.now()}] Rebalancer started: WATCH={WATCH_LIST}, INTERVAL={INTERVAL}s, LEVERAGE={LEVERAGE}")

    # 5) event loop
    while True:
        msg = await ps.get_message(ignore_subscribe_messages=True, timeout=1.0)
        if msg and msg['type'] == 'message':
            payload = json.loads(msg['data'])
            print(f"[{dt.now()}] Tick → {payload['s']} @ {payload['p']}")
            rebalancer.update_price(payload['s'], payload['p'])

        now = dt.utcnow()
        if (now - last_rebalance).total_seconds() >= INTERVAL:
            if rebalancer.should_rebalance(now):
                print(f"[{dt.now()}] → Rebalance triggered")
                await rebalancer.execute()
            last_rebalance = now

        if int(dt.utcnow().timestamp()) % 10 == 0:
            print(f"[{dt.now()}] …waiting for ticks…")

        await asyncio.sleep(0.1)

if __name__ == '__main__':
    asyncio.run(stream_and_rebalance())

def should_rebalance(self, now=None):
    now = now or dt.utcnow()  # Use the current UTC time if 'now' is not provided
    elapsed = (now - self.last_rebalance_time).total_seconds()  # Calculate elapsed time
    filled = [p for p in self.prices.values() if p is not None]  # Filter non-None prices
    return elapsed >= self.min_price_points and len(filled) >= self.min_price_points
