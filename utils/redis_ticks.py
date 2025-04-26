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

async def last_price(symbol: str) -> Optional[float]:
    raw = await aioredis.from_url(REDIS_URL).get(f"tick:last:{symbol}")
    return float(raw) if raw else None

async def main():
    # Example usage of TickCache
    tc = TickCache(["SPY", "QQQ"])
    await tc.start()

    # Now run an endless print loop asynchronously
    while True:
        print("SPY last =", tc.price("SPY"))
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
