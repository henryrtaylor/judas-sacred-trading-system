from __future__ import annotations
import asyncio, json, os, time
from collections import deque
from typing import Dict, Deque, Optional

import redis.asyncio as aioredis

REDIS_URL   = os.getenv("REDIS_URL", "redis://127.0.0.1:6379")
EXPIRE_SEC  = 90                # if last tick is older → fall back / mark guessed

class TickHub:
    """Keeps the most recent tick for every subscribed symbol in memory."""

    def __init__(self, symbols: list[str]) -> None:
        self._symbols      = symbols
        self._latest: Dict[str, Dict] = {}
        self._q: Deque     = deque(maxlen=500)     # optional async queue
        self._rds = aioredis.from_url(REDIS_URL, decode_responses=True)

    async def start(self) -> None:
        pubsub = self._rds.pubsub()
        await pubsub.subscribe(*(f"ticks:{s}" for s in self._symbols))
        asyncio.create_task(self._reader(pubsub))

    async def _reader(self, pubsub) -> None:
        async for msg in pubsub.listen():
            if msg["type"] != "message":
                continue
            tick = json.loads(msg["data"])
            self._latest[tick["s"]] = tick
            self._q.append(tick)        # optional downstream use

    # ------------------------------------------------------------------ #
    def last_price(self, sym: str) -> tuple[Optional[float], bool]:
        """
        Return (price, guessedFlag). If *guessedFlag* is True the price is
        older than ``EXPIRE_SEC`` seconds – caller may treat it as “stale”.
        """
        tick = self._latest.get(sym)
        if not tick:
            return None, True
        age = time.time()*1000 - tick["t"]
        return tick["p"], (age > EXPIRE_SEC*1000)
