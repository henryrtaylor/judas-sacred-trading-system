from ib_insync import *
from config import IBKR_HOST, IBKR_PORT, CLIENT_ID
import pandas as pd
import matplotlib.pyplot as plt
import csv
from pathlib import Path  # ✅ FIXED HERE


# Connect to IBKR
ib = IB()
ib.connect(IBKR_HOST, IBKR_PORT, clientId=CLIENT_ID)

print("✅ Connected. Fetching 30 days of data...")

# Define asset and data request
contract = Stock('AAPL', 'SMART', 'USD')
bars = ib.reqHistoricalData(
    contract,
    endDateTime='',
    durationStr='30 D',
    barSizeSetting='1 hour',
    whatToShow='TRADES',
    useRTH=True,
    formatDate=1
)

ib.disconnect()

# Convert to DataFrame
df = util.df(bars)
df['sma_fast'] = df['close'].rolling(window=5).mean()
df['sma_slow'] = df['close'].rolling(window=15).mean()
df.dropna(inplace=True)

# Initialize backtest variables
position = 0
entry_price = 0
size = 10  # fixed number of shares per trade
equity_curve = []
trade_log = []
signals = []
pnl = []

# Run backtest
for i in range(1, len(df)):
    prev = df.iloc[i - 1]
    curr = df.iloc[i]
    close = curr['close']

    if position == 0 and prev['sma_fast'] < prev['sma_slow'] and curr['sma_fast'] > curr['sma_slow']:
        position = 1
        entry_price = close
        signals.append((curr['date'], 'BUY', close))

    elif position == 1 and prev['sma_fast'] > prev['sma_slow'] and curr['sma_fast'] < curr['sma_slow']:
        position = 0
        signals.append((curr['date'], 'SELL', close))
        trade_return = (close - entry_price) * size
        pnl.append(trade_return)

        # Equity curve
        equity_curve.append(equity_curve[-1] + trade_return if equity_curve else trade_return)

        # Log trade
        trade_log.append({
            'date': curr['date'],
            'entry': round(entry_price, 2),
            'exit': round(close, 2),
            'pnl': round(trade_return, 2)
        })

# Results
print("\n📊 Backtest Summary:")
print(f"Signals: {len(signals)}")
print(f"Trades executed: {len(pnl)}")
if pnl:
    win_rate = sum(1 for x in pnl if x > 0) / len(pnl) * 100
    print(f"Win rate: {win_rate:.2f}%")
    print(f"Net PnL: {sum(pnl):.2f}")
else:
    print("No trades executed.")

# Export trades to CSV
Path("logs").mkdir(exist_ok=True)
with open("logs/backtest_trades.csv", mode="w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["date", "entry", "exit", "pnl"])
    writer.writeheader()
    writer.writerows(trade_log)

print("📝 Trades logged to logs/backtest_trades.csv")

# Plot price + SMAs + signals
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['close'], label='Price', color='gray', alpha=0.5)
plt.plot(df['date'], df['sma_fast'], label='5 SMA', color='blue')
plt.plot(df['date'], df['sma_slow'], label='15 SMA', color='orange')

for t, side, price in signals:
    color = 'green' if side == 'BUY' else 'red'
    marker = '^' if side == 'BUY' else 'v'
    plt.scatter(t, price, color=color, marker=marker, s=80, label=side if t == signals[0][0] else "")

plt.title("Backtest: SMA Crossover – AAPL")
plt.xlabel("Time")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Plot equity curve
plt.figure(figsize=(10, 4))
plt.plot(equity_curve, label='Equity Curve', color='purple')
plt.title("Simulated PnL Over Time")
plt.xlabel("Trade #")
plt.ylabel("PnL")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.show()
