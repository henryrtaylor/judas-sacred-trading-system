# mirror_trader.py
# 🪞 Judas Mirror Trading System (v2) — Sacred Sync Engine ✨

import json
import os
from pathlib import Path
from ib_insync import IB, Stock, MarketOrder
from datetime import datetime
from sacred_logger import log_event

# Load master orders
orders_file = "logs/orders.csv"
followers_file = "configs/follower_accounts.json"

if not os.path.exists(orders_file):
    print("❌ No master orders found to mirror.")
    exit()

# Load follower accounts
try:
    with open(followers_file) as f:
        followers = json.load(f)
except Exception:
    print("❌ Failed to load follower_accounts.json")
    exit()

# Load latest orders
orders = []
with open(orders_file, "r") as f:
    for line in f.readlines()[1:]:  # skip header
        try:
            timestamp, symbol, shares, action, price = line.strip().split(",")
            orders.append({
                "symbol": symbol,
                "shares": int(shares),
                "action": action,
                "price": float(price),
                "timestamp": timestamp
            })
        except ValueError:
            continue  # skip malformed lines

if not orders:
    print("❌ No master orders found to mirror.")
    exit()

# Connect to IBKR paper trading
ib = IB()
try:
    ib.connect("127.0.0.1", 7497, clientId=77)
    print("✅ Connected to IBKR (Paper)")
except Exception as e:
    print(f"❌ Failed to connect to IBKR: {e}")
    exit()

# Process mirror orders
for follower in followers:
    name = follower["name"]
    ratio = follower["ratio"]

    for order in orders[-3:]:  # Only last 3 orders
        shares = max(1, int(order["shares"] * ratio))
        contract = Stock(order["symbol"], "SMART", "USD")
        trade = ib.placeOrder(contract, MarketOrder(order["action"], shares))
        print(f"🪞 Mirroring: {order['action']} {shares} x {order['symbol']} for {name}")
        log_event("mirror", f"{name} mirrored {order['action']} {shares} x {order['symbol']}")

ib.disconnect()
print("✅ All follower orders sent.")
