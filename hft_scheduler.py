
import asyncio
from micro_signal_engine import get_micro_signals
from fast_executor import execute_fast_trade
from judas_config import CONFIG

WATCHLIST = CONFIG.get("watchlist", ['AAPL', 'TSLA', 'NVDA', 'AMD'])

async def pulse():
    while True:
        for symbol in WATCHLIST:
            signal = get_micro_signals(symbol)
            if signal:
                execute_fast_trade(symbol, signal)
        await asyncio.sleep(1)  # Run every second (tweakable)

if __name__ == "__main__":
    print("⚡ HFT Scheduler Live — 1s pulse")
    asyncio.run(pulse())