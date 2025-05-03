import asyncio
import redis.asyncio as aioredis
import random
import json
from datetime import datetime

async def publish_ticks():
    redis_url = "redis://localhost:6379"
    client = aioredis.from_url(redis_url)
    
    symbol = "AAPL"
    base_price = 175.00
    channel = f"T.{symbol}"

    print(f"📡 Publishing simulated ticks for {symbol} on channel '{channel}'...")
    while True:
        # Simulate price drift
        price = round(base_price + random.uniform(-1.5, 1.5), 2)
        tick = json.dumps({"s": symbol, "p": price, "t": datetime.utcnow().isoformat()})

        await client.publish(channel, tick)
        print(f"[FakeTicker] Sent: {tick}")
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(publish_ticks())
