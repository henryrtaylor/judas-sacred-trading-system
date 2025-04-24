import asyncio, json, os
from collections import deque
from typing import Deque, Dict, Optional

import redis.asyncio as aioredis

REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379")

class TickCache:
    """Holds the *latest* tick per symbol in RAM (thread-safe)."""

    def __init__(self, symbols):
        self.latest: Dict[str, float] = {}
        self._q: Deque[tuple[str, float]] = deque(maxlen=1000)
        self._symbols = symbols
        self._task = None

    async def start(self):
        rds = aioredis.from_url(REDIS_URL)
        pub = rds.pubsub()
        await pub.subscribe(*[f"ticks:{s}" for s in self._symbols])

        async def _reader():
            async for msg in pub.listen():
                if msg["type"] != "message":
                    continue
                data = json.loads(msg["data"])
                sym  = data["s"]
                self.latest[sym] = data["p"]
                self._q.append((sym, data["p"]))

        self._task = asyncio.create_task(_reader())

    def price(self, sym: str) -> Optional[float]:
        return self.latest.get(sym)


# Async Redis client
_RDS = aioredis.from_url(REDIS_URL)

async def last_price(symbol: str) -> Optional[float]:
    raw = await _RDS.get(f"tick:last:{symbol}")
    return float(raw) if raw else None

# Synchronous wrapper removed to avoid blocking in async context
# def last_price_sync(symbol: str) -> Optional[float]:
#     return asyncio.run(last_price(symbol))

if __name__ == "__main__":
    import time, asyncio
    tc = TickCache(["SPY", "QQQ"])
    asyncio.run(tc.start())          # fire-and-forget in real code

    while True:
        print("SPY last =", tc.price("SPY"))
        time.sleep(1)
