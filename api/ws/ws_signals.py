import asyncio
import websockets
import json

clients = set()

async def signal_broadcast(data: dict):
    if clients:
        message = json.dumps(data)
        await asyncio.wait([client.send(message) for client in clients])

async def handler(websocket):
    clients.add(websocket)
    try:
        async for _ in websocket:
            pass
    finally:
        clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "localhost", 6789):
        await asyncio.Future()  # keep alive

if __name__ == "__main__":
    asyncio.run(main())
