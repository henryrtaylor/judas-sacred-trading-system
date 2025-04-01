import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
from ib_insync import *
from config import IBKR_HOST, IBKR_PORT, CLIENT_ID, USE_LIVE_TRADING, MIN_ORDER_DOLLARS, MAX_ORDER_DOLLARS
from goals import TARGET_ALLOCATION
import argparse
from pathlib import Path
from datetime import datetime

# --- CLI ARGUMENTS ---
parser = argparse.ArgumentParser(description="Auto-execute portfolio rebalance trades.")
parser.add_argument('--dry-run', action='store_true', help='Preview trades without executing')
args = parser.parse_args()

# --- SAFETY NOTICE ---
if USE_LIVE_TRADING:
    print("⚠️ WARNING: LIVE TRADING MODE ENABLED ⚠️")
else:
    print("🔁 Paper trading mode active (safe sandbox)")

# --- LOAD PORTFOLIO SNAPSHOT ---
try:
    df = pd.read_csv("logs/portfolio_snapshot.csv")
except FileNotFoundError:
    print("❌ No portfolio snapshot found. Run analyze_portfolio_fallback.py first.")
    exit()

df['symbol'] = df['symbol'].str.upper()
portfolio_value = df['est_value'].sum()
actual_allocation = dict(zip(df['symbol'], df['pct_of_portfolio'] / 100))
actual_allocation['CASH'] = 1 - sum(actual_allocation.values())

# --- CONNECT TO IBKR ---
ib = IB()
ib.connect(IBKR_HOST, IBKR_PORT, clientId=CLIENT_ID)
print("✅ Connected to IBKR for execution\n")

# --- EXECUTION LOG SETUP ---
Path("logs").mkdir(exist_ok=True)
log_path = Path("logs/orders.csv")
log_exists = log_path.exists()
log_writer = []

# --- EXECUTION LOGIC ---
for symbol, target_pct in TARGET_ALLOCATION.items():
    symbol = symbol.upper()

    if symbol == "CASH":
        continue

    actual_pct = actual_allocation.get(symbol, 0)
    delta_pct = target_pct - actual_pct

    if delta_pct < 0.01:
        continue

    allocation_dollars = delta_pct * portfolio_value
    if allocation_dollars < MIN_ORDER_DOLLARS:
        print(f"⚠️ Skipping {symbol}: suggested trade below ${MIN_ORDER_DOLLARS}")
        continue
    if allocation_dollars > MAX_ORDER_DOLLARS:
        print(f"⛔ Skipping {symbol}: trade exceeds max allowed ${MAX_ORDER_DOLLARS}")
        continue

    contract = Stock(symbol, 'SMART', 'USD')
    ib.qualifyContracts(contract)

    try:
        mkt_data = ib.reqMktData(contract, '', False, False)
        ib.sleep(1)

        price = mkt_data.marketPrice()
        if price is None or pd.isna(price):
            match = df[df['symbol'] == symbol]
            if not match.empty:
                price = match.iloc[0]['avgCost']
            else:
                raise ValueError("No fallback price available.")

    except Exception as e:
        print(f"⚠️ Skipping {symbol}: price fetch failed. {e}")
        continue

    shares = int(allocation_dollars / price)
    if shares < 1:
        print(f"⚠️ Skipping {symbol}: fewer than 1 share to buy.")
        continue

    order = MarketOrder("BUY", shares)

    if args.dry_run:
        print(f"🧪 DRY RUN: Buy {shares} x {symbol} @ est ${price:.2f}")
        status = "SIMULATED"
    else:
        print(f"🚀 Executing: Buy {shares} x {symbol} @ market")
        trade = ib.placeOrder(contract, order)
        ib.sleep(2)
        status = trade.orderStatus.status

    log_writer.append({
        "time": datetime.now().isoformat(),
        "symbol": symbol,
        "shares": shares,
        "action": "BUY",
        "orderType": "Market",
        "estPrice": round(price, 2),
        "status": status
    })

# --- SAVE LOG ---
log_df = pd.DataFrame(log_writer)
log_df.to_csv(log_path, mode="a", header=not log_exists, index=False)
print("\n📦 Order log saved to logs/orders.csv")

ib.disconnect()
