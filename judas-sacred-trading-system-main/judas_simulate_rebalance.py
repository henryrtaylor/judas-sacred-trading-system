# judas_simulate_rebalance.py
# 📈 Judas Sacred Rebalance Simulator with Reinforcement Upgrade

import pandas as pd
import json
from datetime import datetime
from pathlib import Path

# Load sacred allocation
with open("generated/generated_goals.json") as f:
    goals = json.load(f)

# Load fallback portfolio
try:
    with open("logs/portfolio_snapshot.json") as f:
        portfolio = json.load(f)
except FileNotFoundError:
    print("⚠️ No portfolio snapshot found. Using dummy fallback portfolio.")
    portfolio = {
        "QQQ": {"qty": 10, "est_value": 1400.00},
        "CASH": {"qty": 0, "est_value": 100.00}
    }

# Load prices
df_prices = pd.read_csv("logs/historical_prices.csv")
df_prices = df_prices[df_prices['symbol'].isin(goals.keys())]
latest_prices = df_prices.groupby("symbol")['close'].last().to_dict()

# Simulate rebalanced portfolio
portfolio_value = sum(v['est_value'] for v in portfolio.values())
rebalanced_portfolio = {}

for symbol, pct in goals.items():
    price = latest_prices.get(symbol)
    if price is None or price == 0:
        continue
    alloc_dollars = pct * portfolio_value
    shares = round(alloc_dollars / price, 2)
    rebalanced_portfolio[symbol] = {
        "shares": shares,
        "price": price,
        "alloc_dollars": round(alloc_dollars, 2)
    }

# Calculate estimated performance
estimated_value = sum(v['shares'] * v['price'] for v in rebalanced_portfolio.values())
change_pct = ((estimated_value - portfolio_value) / portfolio_value) * 100

# Log simulation
Path("logs").mkdir(exist_ok=True)
sim_log = {
    "timestamp": datetime.now().isoformat(),
    "initial_value": round(portfolio_value, 2),
    "simulated_value": round(estimated_value, 2),
    "change_pct": round(change_pct, 2),
    "allocations": goals
}

with open("logs/judas_simulation_log.json", "w") as f:
    json.dump(sim_log, f, indent=4)

print("\n🔮 Judas Reinforced Simulation Summary")
print("----------------------------------------")
print(f"💼 Portfolio Value: ${portfolio_value:,.2f}")
print(f"📈 Simulated Value: ${estimated_value:,.2f}")
print(f"📊 Change: {change_pct:+.2f}%")
print("\n🧾 Rebalanced Holdings:")
for sym, data in rebalanced_portfolio.items():
    print(f"➡️  {sym}: {data['shares']} x ${data['price']:.2f} = ${data['alloc_dollars']:.2f}")

print("\n✅ Simulation saved to logs/judas_simulation_log.json")
