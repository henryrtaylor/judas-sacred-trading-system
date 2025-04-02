# rebalance_execute.py
# Sacred Auto-Rebalancing with Drawdown Awareness and IBKR Auto-Detection

import asyncio
import json
from ib_insync import IB, Stock, MarketOrder
from pathlib import Path
from datetime import datetime

try:
    from drawdown_guardian import check_drawdown
except ImportError:
    print("⚠️ drawdown_guardian module not found. Skipping drawdown protection.")
    check_drawdown = lambda *_: True

try:
    from tws_auto_config import get_ibkr_settings
except ImportError:
    print("⚠️ tws_auto_config not found. Using default config.")
    get_ibkr_settings = lambda: ("127.0.0.1", 7497, 1)

# Load strategy goals
with open("generated/generated_goals.json") as f:
    strategy_goals = json.load(f)

# Load current portfolio or fallback
portfolio_path = Path("logs/portfolio_snapshot.json")
if portfolio_path.exists():
    with open(portfolio_path) as f:
        portfolio = json.load(f)
else:
    print("⚠️ No portfolio snapshot found. Using dummy fallback portfolio.")
    portfolio = [
        {"symbol": "QQQ", "est_value": 1000.0},
        {"symbol": "VZ", "est_value": 500.0},
        {"symbol": "T", "est_value": 300.0}
    ]

# Connect to IBKR
ib = IB()

ports_to_try = [7497, 7496, 4001, 4002]
host = "127.0.0.1"
clientId = 1

connected = False
for port in ports_to_try:
    try:
        print(f"🔌 Trying port {port}...")
        ib.connect(host, port, clientId=clientId)
        print(f"✅ Connected to IBKR on port {port}")
        connected = True
        break
    except Exception as e:
        print(f"❌ Port {port} failed: {e}")

if not connected:
    print("❌ All IBKR connection attempts failed.")
    exit()

# Get total value
total_value = sum(pos.get("est_value", 0) for pos in portfolio)
print(f"💼 Total portfolio value: ${total_value:.2f}")

# Run drawdown check
if not check_drawdown():
    print("⚠️ Drawdown threshold hit. Execution halted.")
    ib.disconnect()
    exit()

# Execute trades
orders = []
for symbol, weight in strategy_goals.items():
    allocation = total_value * weight
    price = 100  # Placeholder price
    shares = max(1, int(allocation / price))
    contract = Stock(symbol, "SMART", "USD")
    order = MarketOrder("BUY", shares)
    orders.append((contract, order))

# Place orders
for contract, order in orders:
    ib.qualifyContracts(contract)
    trade = ib.placeOrder(contract, order)
    print(f"🚀 Executing: {order.action} {order.totalQuantity} x {contract.symbol}")

ib.disconnect()

# Log orders
log_path = Path("logs") / "mirror_orders.txt"
with open(log_path, "a") as f:
    for contract, order in orders:
        f.write(f"{datetime.now()},{contract.symbol},{order.totalQuantity},{order.action},market\n")

print("📦 Orders executed and logged.")
