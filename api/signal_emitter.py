
import asyncio
import json
import websockets
import random
import datetime

async def emit_signals():
    uri = "ws://localhost:8000/ws/signals"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                while True:
                    mock_signal = {
                        "symbol": random.choice(["AAPL", "TSLA", "NVDA"]),
                        "action": random.choice(["BUY", "SELL"]),
                        "confidence": round(random.uniform(0.5, 1.0), 2),
                        "timestamp": datetime.datetime.utcnow().isoformat()
                    }
                    await websocket.send(json.dumps(mock_signal))
                    await asyncio.sleep(3)
        except Exception as e:
            print(f"WebSocket connection failed: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(emit_signals())
