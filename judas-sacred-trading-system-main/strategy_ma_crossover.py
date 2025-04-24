from ib_insync import *
from config import IBKR_HOST, IBKR_PORT, CLIENT_ID
import pandas as pd
import matplotlib.pyplot as plt

# Connect to IBKR
ib = IB()
ib.connect(IBKR_HOST, IBKR_PORT, clientId=CLIENT_ID)

print("✅ Connected. Requesting historical data...")

# Choose asset and time frame
contract = Stock('AAPL', 'SMART', 'USD')
bars = ib.reqHistoricalData(
    contract,
    endDateTime='',
    durationStr='2 D',
    barSizeSetting='5 mins',
    whatToShow='TRADES',
    useRTH=True,
    formatDate=1
)

# Convert to DataFrame
df = util.df(bars)
df['sma_fast'] = df['close'].rolling(window=5).mean()
df['sma_slow'] = df['close'].rolling(window=15).mean()

# Check latest crossover
last = df.iloc[-1]
prev = df.iloc[-2]

signal = None

if prev['sma_fast'] < prev['sma_slow'] and last['sma_fast'] > last['sma_slow']:
    signal = 'BUY'
elif prev['sma_fast'] > prev['sma_slow'] and last['sma_fast'] < last['sma_slow']:
    signal = 'SELL'

print(f"\n📊 Strategy Signal: {signal or 'No Signal'}")

# Place order (paper trading only)
if signal == 'BUY':
    order = MarketOrder('BUY', 10)
    trade = ib.placeOrder(contract, order)
    print("🚀 Placing BUY order")
elif signal == 'SELL':
    order = MarketOrder('SELL', 10)
    trade = ib.placeOrder(contract, order)
    print("🔻 Placing SELL order")

# Plot chart
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['close'], label='Price', color='gray', alpha=0.7)
plt.plot(df['date'], df['sma_fast'], label='5 SMA', color='blue')
plt.plot(df['date'], df['sma_slow'], label='15 SMA', color='orange')

# Plot signal marker if exists
if signal == 'BUY':
    plt.scatter(last['date'], last['close'], color='green', label='Buy Signal', marker='^', s=100)
elif signal == 'SELL':
    plt.scatter(last['date'], last['close'], color='red', label='Sell Signal', marker='v', s=100)

plt.title('SMA Crossover Strategy – AAPL')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

ib.disconnect()
