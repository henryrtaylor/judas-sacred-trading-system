import pandas as pd
from goals import TARGET_ALLOCATION

# Load fallback portfolio from analyze_portfolio_fallback.py
portfolio_df = pd.read_csv("logs/portfolio_snapshot.csv")  # We'll output this if needed

# Calculate actual allocation
portfolio_df['actual_pct'] = portfolio_df['pct_of_portfolio'] / 100
portfolio_df['symbol'] = portfolio_df['symbol'].str.upper()

# Create current allocation dictionary
actual_allocation = dict(zip(portfolio_df['symbol'], portfolio_df['actual_pct']))
cash_weight = 1 - sum(actual_allocation.values())
actual_allocation['CASH'] = cash_weight

# Rebalance logic
print("📊 --- Rebalance Recommendation ---\n")
for symbol, target_pct in TARGET_ALLOCATION.items():
    actual_pct = actual_allocation.get(symbol, 0)
    diff = target_pct - actual_pct
    diff_dollars = diff * portfolio_df['est_value'].sum() / (1 - cash_weight)

    direction = "✅ Aligned"
    if diff > 0.01:
        direction = f"🟢 Increase {symbol} by ~${diff_dollars:,.2f}"
    elif diff < -0.01:
        direction = f"🔻 Decrease {symbol} by ~${abs(diff_dollars):,.2f}"

    print(f"{symbol}: Target = {target_pct:.0%} | Actual = {actual_pct:.0%} → {direction}")

print("\n🧠 Powered by Judas the Treasurer — Align with your destiny.")
