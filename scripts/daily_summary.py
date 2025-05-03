import os
import asyncio
from ib_insync import IB
from dotenv import load_dotenv
import aiohttp
from datetime import datetime as dt
import nest_asyncio

load_dotenv()
nest_asyncio.apply()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
IB_HOST = os.getenv("IBKR_HOST", "127.0.0.1")
IB_PORT = int(os.getenv("IBKR_API_PORT", "7497"))
IB_CLIENT_ID = int(os.getenv("IBKR_CLIENT_ID", "222"))

async def send_telegram(msg: str):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    async with aiohttp.ClientSession() as session:
        await session.post(url, json=payload)

async def generate_daily_summary():
    ib = IB()
    try:
        await asyncio.wait_for(ib.connectAsync(IB_HOST, IB_PORT, clientId=IB_CLIENT_ID), timeout=5)
    except asyncio.TimeoutError:
        await send_telegram("❌ Status check failed: IBKR connection timed out.")
        return

    account = ib.managedAccounts()[0]
    raw_summary = ib.accountSummary(account)
    summary = {item.tag: float(item.value) for item in raw_summary if item.value.replace('.', '', 1).isdigit()}
    positions = ib.positions(account)

    value = summary.get('NetLiquidation', 0.0)
    start = summary.get('DayStartingValue', value)
    pnl = summary.get('RealizedPnL', 0.0)

    change = value - start
    pct = (change / start * 100) if start else 0.0

    gainers, losers = [], []
    for p in positions:
        contract = p.contract
        ticker = ib.reqMktData(contract, '', False, False)
        await asyncio.sleep(0.5)
        market_price = ticker.marketPrice()
        if market_price is None or market_price == 0.0:
            gainers.append(p.contract.symbol + " (?)")
            continue
        unrealized = (market_price - p.avgCost) * p.position
        if unrealized >= 0:
            gainers.append(p.contract.symbol)
        else:
            losers.append(p.contract.symbol)

    msg = f"\U0001F4CA Daily P&L Report ({dt.now().strftime('%b %d')})\n"
    msg += f"\U0001F9BE Value: ${value:,.2f}\n"
    msg += f"{'🟢' if change >= 0 else '🔴'} Change: ${change:,.2f} ({pct:.2f}%)\n\n"
    if gainers:
        msg += f"🟢 Gainers: {', '.join(gainers)}\n"
    if losers:
        msg += f"🔴 Losers: {', '.join(losers)}\n"
    msg += f"📦 Holdings: {len(positions)} positions"

    await send_telegram(msg)
    ib.disconnect()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(generate_daily_summary())
