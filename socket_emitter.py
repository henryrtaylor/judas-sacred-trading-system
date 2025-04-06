# socket_emitter.py

import asyncio
import websockets
import json

async def _emit(event):
    try:
        async with websockets.connect("ws://localhost:6789") as ws:
            await ws.send(json.dumps(event))
    except Exception as e:
        print(f"⚠️ Socket emit failed: {e}")

def emit_socket(event: dict):
    asyncio.run(_emit(event))