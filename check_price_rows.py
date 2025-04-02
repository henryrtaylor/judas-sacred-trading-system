import pandas as pd

# Load the historical prices CSV
try:
    df = pd.read_csv("logs/historical_prices.csv", parse_dates=["date"])
    df['close'] = pd.to_numeric(df['close'], errors='coerce')  # Force float conversion
except Exception as e:
    print(f"❌ Error loading price data: {e}")
    exit()

# Count valid (non-NaN) close prices for each symbol
summary = (
    df.groupby("symbol")['close']
    .apply(lambda x: x.dropna().shape[0])
    .reset_index(name="valid_rows")
)

# Display results
print("\n📊 Symbol Row Counts (Valid 'close' entries):\n")
print(summary.to_string(index=False))
