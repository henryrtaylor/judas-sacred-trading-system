
import asyncio
from api.ws_signals import broadcast_signal

async def fake_signal_loop():
    import random
    import datetime

    symbols = ["AAPL", "TSLA", "NVDA", "AMD"]
    signals = ["BUY", "SELL", "HOLD"]

    while True:
        signal_data = {
            "symbol": random.choice(symbols),
            "signal": random.choice(signals),
            "timestamp": datetime.datetime.now().isoformat()
        }
        print(f"📡 Sending fake signal: {signal_data}")
        await broadcast_signal(signal_data)
        await asyncio.sleep(5)
