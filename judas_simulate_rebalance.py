"""
🔮 Judas Simulate Rebalance 🔮
Simulates reallocation based on strategy engine output and current portfolio snapshot.
Handles sacred numbers, errors, and intention.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import pandas as pd
import json
from pathlib import Path
from datetime import datetime

# 📁 Paths
portfolio_file = Path("logs/portfolio_snapshot.csv")
goals_file = Path("generated/generated_goals.json")
log_file = Path("logs/judas_simulation_log.json")

# 📦 Load portfolio
try:
    portfolio = pd.read_csv(portfolio_file)
    portfolio.columns = [c.strip() for c in portfolio.columns]
    portfolio = portfolio.rename(columns={"est_value": "marketValue"})  # ensure uniformity
except Exception as e:
    print(f"❌ Failed to load portfolio: {e}")
    exit(1)

# 💼 Calculate portfolio value
if "marketValue" not in portfolio.columns:
    print("❌ 'marketValue' column missing in portfolio.")
    exit(1)

total_value = portfolio["marketValue"].sum()
print(f"\n🧪 Judas Simulation Summary\n💼 Portfolio Value: ${total_value:,.2f}")

# 🎯 Load strategy allocation
try:
    with open(goals_file, "r", encoding="utf-8") as f:
        target_alloc = json.load(f)
except Exception as e:
    print(f"❌ Failed to load strategy output: {e}")
    exit(1)

# 🧾 Simulate Rebalance
simulated_orders = []
for symbol, target_pct in target_alloc.items():
    allocation_dollars = total_value * (target_pct / 100)
    simulated_orders.append({
        "symbol": symbol,
        "target_pct": target_pct,
        "allocation": round(allocation_dollars, 2)
    })

print("\n🧾 Rebalancing Orders:")
for order in simulated_orders:
    print(f"➡️ BUY  ${order['allocation']:,.2f} of {order['symbol']}")

# 📜 Save to log
log_file.parent.mkdir(exist_ok=True)
log_entry = {
    "timestamp": datetime.now().isoformat(),
    "portfolio_value": total_value,
    "orders": simulated_orders
}

with open(log_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(log_entry) + "\n")

print(f"\n✅ Simulation saved to {log_file}")
