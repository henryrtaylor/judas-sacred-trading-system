import asyncio
import websockets
import json
from datetime import datetime

async def emit_signals():
    uri = "ws://localhost:8000/ws/signals"
    while True:
        signal = {
            "symbol": "AAPL",
            "action": "BUY",
            "confidence": 0.93,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        try:
            async with websockets.connect(uri) as websocket:
                await websocket.send(json.dumps(signal))
                print("🚀 Sent signal:", signal)
        except Exception as e:
            print("❌ Could not send signal:", e)
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(emit_signals())
