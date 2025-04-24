# utils/polygon_ws_publisher.py

import asyncio
import json
import os
import websockets
import redis.asyncio as aioredis

POLY_KEY   = os.getenv("POLYGON_API_KEY")
SYMBOLS    = os.getenv("WATCH_LIST", "SPY,QQQ,TLT,GLD").split(',')
REDIS_URL  = os.getenv("REDIS_URL", "redis://127.0.0.1:6379")

async def publisher():
    print("[Publisher] Connecting to Redis…")
    redis = aioredis.from_url(REDIS_URL)

    uri = "wss://socket.polygon.io/stocks"
    print(f"[Publisher] Connecting to Polygon WS at {uri}…")
    async with websockets.connect(uri) as ws:
        print("[Publisher] Sending auth…")
        await ws.send(json.dumps({"action": "auth", "params": POLY_KEY}))
        print("[Publisher] Auth sent, subscribing…")
        symbols_param = ",".join(f"T.{s}" for s in SYMBOLS)
        await ws.send(json.dumps({"action": "subscribe", "params": symbols_param}))
        print(f"[Publisher] Subscribed to: {symbols_param}")

        async for message in ws:
            # **Raw debug** before parsing
            print("[Publisher raw]", message)
            try:
                data = json.loads(message)
            except Exception as e:
                print("[Publisher] JSON error:", e)
                continue

            for evt in data:
                symbol = evt.get("sym") or evt.get("S")
                price  = evt.get("p")
                if symbol and price is not None:
                    print(f"[Publisher] → {symbol}@{price}")
                    await redis.publish(f"ticks:{symbol}", json.dumps({"s": symbol, "p": price}))

if __name__ == "__main__":
    asyncio.run(publisher())
