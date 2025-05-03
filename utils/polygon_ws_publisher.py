import asyncio
import json
import os
import websockets
import redis.asyncio as aioredis

POLY_KEY = os.getenv("POLYGON_API_KEY")
STOCKS = SYMBOLS = ["SPY", "QQQ", "TLT", "GLD"]
CRYPTOS = ["BTC-USD", "ETH-USD"]
REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6380")

async def wait_for_auth(ws):
    while True:
        msg = await ws.recv()
        data = json.loads(msg)
        print("[Publisher] Auth check:", data)
        if any(d.get('status') == 'auth_success' for d in (data if isinstance(data, list) else [data])):
            print("[Publisher] Authenticated!")
            return

async def publisher(endpoint, symbols, is_crypto=False):
    while True:
        try:
            print(f"[Publisher] Connecting to Redis...")
            redis = aioredis.from_url(REDIS_URL)

            uri = f"wss://socket.polygon.io/{endpoint}"
            print(f"[Publisher] Connecting to {uri}...")
            async with websockets.connect(uri) as ws:
                await ws.send(json.dumps({"action": "auth", "params": POLY_KEY}))
                await wait_for_auth(ws)

                # Build subscription string
                if is_crypto:
                    symbols_param = ",".join(f"XT.{s}" for s in symbols) + "," + ",".join(f"XA.{s}" for s in symbols)
                else:
                    symbols_param = ",".join(f"T.{s}" for s in symbols)

                await ws.send(json.dumps({"action": "subscribe", "params": symbols_param}))
                print(f"[Publisher] Subscribed: {symbols_param}")

                async for message in ws:
                    try:
                        data = json.loads(message)
                        for evt in data:
                            symbol = evt.get("sym") or evt.get("S")
                            price = evt.get("p")
                            if symbol and price is not None:
                                print(f"[Publisher] → {symbol}@{price}")
                                await redis.publish(f"ticks:{symbol}", json.dumps({"s": symbol, "p": price}))
                    except Exception as e:
                        print("[Publisher] JSON parse error:", e)
        except Exception as e:
            print(f"[Publisher] Connection error: {e}")
            await asyncio.sleep(5)

async def main():
    await asyncio.gather(
        publisher("stocks", STOCKS),
        publisher("crypto", CRYPTOS, is_crypto=True)
    )

if __name__ == "__main__":
    asyncio.run(main())
