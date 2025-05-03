#!/usr/bin/env python
import os
import sys
import logging
import asyncio
import json
import redis.asyncio as aioredis
from datetime import datetime as dt
from dotenv import load_dotenv
load_dotenv()  # loads .env into os.environ

# ensure project root is on sys.path for local module imports
sys.path.insert(0, os.path.abspath(os.path.join(__file__, '..')))

from ib_insync import IB
from judas_ibkr.rebalancer import Rebalancer
import aiohttp

# Disable IB destructor to prevent "Event loop is closed" errors
from ib_insync import IB as _IB
_IB.__del__ = lambda self: None

# Logging setup: file + console
os.makedirs('logs', exist_ok=True)
formatter = logging.Formatter('[%(asctime)s] %(message)s')
file_handler = logging.FileHandler('logs/rebalancer.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(logging.DEBUG)
root.addHandler(file_handler)
root.addHandler(console_handler)
logger = logging.getLogger(__name__)

# Telegram setup
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

async def send_telegram(message: str):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        logger.debug("Telegram creds missing, skipping message.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    async with aiohttp.ClientSession() as session:
        await session.post(url, json=payload)
    logger.debug(f"Sent Telegram: {message}")

async def send_watchlist():
    """Send the current WATCH_LIST via Telegram."""
    wl = os.getenv('WATCH_LIST', '')
    tickers = [s for s in wl.split(',') if s]
    lines = "\n".join(f"• {s}" for s in tickers)
    reply = f"🎯 Current WATCH_LIST:\n{lines}"
    await send_telegram(reply)

# Strategy parameters
WATCH_LIST        = os.getenv('WATCH_LIST', 'SPY,QQQ,TLT,GLD').split(',')
REDIS_URL         = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379')
IB_HOST           = os.getenv('IBKR_HOST', '127.0.0.1')
IB_PORT           = int(os.getenv('IBKR_API_PORT', '7497'))
IB_CLIENT_ID      = int(os.getenv('IBKR_CLIENT_ID', '1'))
INTERVAL          = int(os.getenv('REBALANCE_INTERVAL', '60'))
MIN_PRICE_POINTS  = int(os.getenv('MIN_PRICE_POINTS', '4'))

async def main():
    redis = aioredis.from_url(REDIS_URL)
    ps = redis.pubsub()
    await ps.subscribe(*[f"ticks:{s}" for s in WATCH_LIST])
    if any('-USD' in s for s in WATCH_LIST):
        await ps.subscribe(*[f"ticks:CRYPTO:{s}" for s in WATCH_LIST if '-USD' in s])
    logger.info(f"Subscribed to ticks channels: {WATCH_LIST}")

    ib = IB()
    await ib.connectAsync(IB_HOST, IB_PORT, clientId=IB_CLIENT_ID)
    logger.info(f"Connected to IBKR: {ib.isConnected()}")

    reb = Rebalancer(
        WATCH_LIST,
        MIN_PRICE_POINTS,
        ib
    )
    # Track orders executed in each rebalance
    orders_executed: list[tuple[str,int,float]] = []
    import judas_ibkr.safe_order as so_mod
    real_safe_execute = so_mod.safe_execute
    def tracking_safe_execute(ib_obj, sym, delta, price, log_flag):
        # record order
        orders_executed.append((sym, delta, price))
        # execute original, schedule if async
        res = real_safe_execute(ib_obj, sym, delta, price, log_flag)
        if asyncio.iscoroutine(res):
            asyncio.create_task(res)
        return res
    so_mod.safe_execute = tracking_safe_execute

    from utils.redis_ticks import last_price
    for s in WATCH_LIST:
        p = await last_price(s)
        if p is not None:
            reb.update_price(s, p)
    logger.info("Rebalancer seeded with last prices.")

    try:
        while True:
            msg = await ps.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if msg and msg['type'] == 'message':
                data = json.loads(msg['data'])
                logger.debug(f"Tick → {data['s']} @ {data['p']}")
                symbol = data.get('s') or data.get('symbol')
                price = data.get('p') or data.get('price')
                if not symbol or not price:
                    logger.warning("⚠️ Malformed tick ignored")
                    continue
                if symbol not in WATCH_LIST:
                    warn = f"⚠️ Ignored tick for untracked symbol: {symbol}"
                    logger.warning(warn)
                    await send_telegram(warn)
                    continue
                reb.update_price(symbol, price)

            now = dt.utcnow()
            elapsed = (now - reb.last_rebalance_time).total_seconds()
            if elapsed >= INTERVAL and reb.should_rebalance(now):
                logger.info("Triggering rebalance event.")
                await send_telegram("🔔 Judas is starting a rebalance…")
                await reb.execute()

                # send order summary
                if orders_executed:
                    for sym, delta, price in orders_executed:
                        side = 'BUY' if delta > 0 else 'SELL'
                        qty = abs(delta)
                        msg = f"{side} {qty} {sym} @ {price:.2f}"
                        logger.info(f"Sending Telegram order: {msg}")
                        await send_telegram(msg)
                    orders_executed.clear()
                else:
                    logger.info("No orders executed this rebalance.")

            if int(dt.utcnow().timestamp()) % 10 == 0:
                logger.debug("…waiting for ticks…")

            await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        logger.info("Shutdown requested.")
    except Exception as e:
        logger.error(f"Fatal error in main loop: {e}")
        # Notify via Telegram
        await send_telegram(f"🚨 Fatal error in main loop: {e}")
    finally:
        if ib.isConnected():
            ib.disconnect()
            logger.info("Disconnected from IBKR.")

if __name__ == '__main__':
    import sys
    if '--watchlist' in sys.argv:
        asyncio.run(send_watchlist())
        sys.exit(0)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted by user.")
    except Exception as e:
        logger.error(f"Stream error: {e}")

