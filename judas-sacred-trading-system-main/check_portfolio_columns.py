import pandas as pd

df = pd.read_csv("logs/portfolio_snapshot.csv")
print("📋 Portfolio Columns:\n", df.columns.tolist())
