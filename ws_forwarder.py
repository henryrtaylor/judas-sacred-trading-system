import json
import asyncio
import websockets

connected_clients = set()

async def broadcast(message: dict):
    if connected_clients:
        data = json.dumps(message)
        await asyncio.wait([client.send(data) for client in connected_clients])

async def handler(websocket, path):
    connected_clients.add(websocket)
    try:
        async for _ in websocket:
            pass  # No incoming messages expected for now
    finally:
        connected_clients.remove(websocket)

def start_ws_server():
    print("🛸 Launching Cosmic Signal Bridge on ws://localhost:6789")
    return websockets.serve(handler, "localhost", 6789)