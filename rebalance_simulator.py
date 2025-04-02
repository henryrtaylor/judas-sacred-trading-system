import pandas as pd
import argparse
from goals import TARGET_ALLOCATION

# --- CLI Input Setup ---
parser = argparse.ArgumentParser(description="Simulate rebalancing using fresh capital")
parser.add_argument('--cash', type=float, default=0, help='New deposit or available cash')
parser.add_argument('--dividends', type=float, default=0, help='Expected or available dividends')
args = parser.parse_args()

available_funds = args.cash + args.dividends

if available_funds <= 0:
    print("⚠️ Simulating without capital (symbolic run).")
    available_funds = 1  # symbolic amount to enable logic flow

print(f"\n💰 Total Funds to Simulate: ${available_funds:,.2f}\n")

# --- Load Current Portfolio Snapshot ---
try:
    df = pd.read_csv("logs/portfolio_snapshot.csv")
except FileNotFoundError:
    print("❌ Portfolio snapshot not found. Run analyze_portfolio_fallback.py first.")
    exit()

df['symbol'] = df['symbol'].str.upper()
actual_alloc = dict(zip(df['symbol'], df['pct_of_portfolio'] / 100))
actual_alloc['CASH'] = 1 - sum(actual_alloc.values())

# --- Simulate Allocation Delta ---
recommendations = []

for symbol, target_pct in TARGET_ALLOCATION.items():
    actual_pct = actual_alloc.get(symbol, 0)
    delta_pct = target_pct - actual_pct

    if delta_pct > 0.005:
        allocation_dollars = delta_pct * available_funds
        recommendations.append({
            'symbol': symbol,
            'current': f"{actual_pct:.1%}",
            'target': f"{target_pct:.1%}",
            'suggested_buy': round(allocation_dollars, 2)
        })

# --- Output Recommendation ---
if recommendations:
    print("📊 --- Judas Rebalance Simulation ---")
    for r in recommendations:
        print(f"🟢 {r['symbol']}: {r['current']} ➜ {r['target']} → Allocate ~${r['suggested_buy']:,.2f}")
else:
    print("✅ Portfolio is already aligned or no significant gaps found.")

print("\n🧠 Simulated using available funds. Judas stands ready.")
