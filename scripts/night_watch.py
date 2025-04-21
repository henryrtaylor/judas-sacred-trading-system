# ---------- night_watch.py ----------
"""After‑hours sentinel.

Runs in a loop every X minutes and pushes Telegram alerts on large moves
in crypto or futures.
"""
import argparse, asyncio, logging
from datetime import datetime
from random import random

TELEGRAM_ID = "6598476266"

async def send_telegram(msg: str):
    # placeholder – replace with real send
    print(f"[TELEGRAM] {msg}")

async def monitor(loop_delay: int):
    while True:
        # placeholder pseudo‑price moves
        btc_move = random() * 0.05  # 0 – 5 %
        if btc_move > 0.03:
            await send_telegram(f"⚠️ BTC moved {btc_move*100:.1f}% after hours @ {datetime.utcnow()} UTC")
        await asyncio.sleep(loop_delay)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--delay", type=int, default=300, help="Loop delay seconds")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="[NIGHT‑WATCH] %(message)s")
    asyncio.run(monitor(args.delay))
