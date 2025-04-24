#!/usr/bin/env python
"""
Subscribe to Interactive‑Brokers tick‑by‑tick data and publish each tick
to Redis (*channel = "ticks:*symbol*"*).

• Requires: ib_insync, redis‑py
• Run once at start‑of‑day; reconnect logic handles TWS restarts.
"""
import asyncio, json, os, time
from datetime import datetime as dt

from ib_insync import IB, Stock, util
import redis.asyncio as aioredis               # redis‑py ≥ 4.2

# ── symbols we really stream ─────────────────────────────────────────
SYMBOLS = [
    "AAPL", "GLD", "NVDA", "QQQ", "SPY",  # alphabetical for clarity
]
# (Crypto removed for now; can be re‑enabled once permissions are added)

REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379")


async def main() -> None:
    """Main reconnect loop – keeps streams alive and republishes ticks."""
    rds = aioredis.from_url(REDIS_URL)
    ib: IB = IB()

    while True:  # auto‑reconnect loop
        try:
            if not ib.isConnected():
                print("🔌 connecting TWS …")
                await ib.connectAsync("127.0.0.1", 7497, clientId=11)
                ib.reqMarketDataType(1)  # 1 = live, 4 = delayed‑frozen

                for sym in SYMBOLS:
                    contract = Stock(sym, "SMART", "USD")
                    ib.reqTickByTickData(
                        contract,
                        tickType="Last",
                        numberOfTicks=0,
                        ignoreSize=True,
                    )

            # Drain the IB event queue and publish to Redis
            await asyncio.sleep(0.02)
            for tick in ib.pendingTickers():
                if not tick.last or tick.last <= 0:
                    continue
                msg = {
                    "t": int(tick.time.timestamp() * 1000),  # epoch‑ms
                    "p": tick.last,
                    "s": tick.contract.symbol,
                    "sz": tick.lastSize,
                }
                channel = f"ticks:{tick.contract.symbol}"
                await rds.publish(channel, json.dumps(msg))
                # cache latest price (30 s expiry)
                await rds.set(f"tick:last:{tick.contract.symbol}", tick.last, ex=30)

        except Exception as exc:
            print("⚠️ tick streamer error:", exc)
            ib.disconnect()
            await asyncio.sleep(5)  # back‑off before retry


if __name__ == "__main__":
    util.patchAsyncio()  # ib_insync helper integrates asyncio loop
    asyncio.run(main())
