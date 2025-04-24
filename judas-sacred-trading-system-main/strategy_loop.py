from ib_insync import *
from config import IBKR_HOST, IBKR_PORT, CLIENT_ID
import pandas as pd
import matplotlib.pyplot as plt
import time

# Connect to IBKR
ib = IB()
ib.connect(IBKR_HOST, IBKR_PORT, clientId=CLIENT_ID)

# Define the asset
contract = Stock('AAPL', 'SMART', 'USD')

print("🚀 Strategy loop started. Checking every 5 minutes...\n(Press CTRL+C to stop)\n")

try:
    while True:
        print("⏳ Checking for signals...")

        # Request historical data
        bars = ib.reqHistoricalData(
            contract,
            endDateTime='',
            durationStr='2 D',
            barSizeSetting='5 mins',
            whatToShow='TRADES',
            useRTH=True,
            formatDate=1
        )

        # Convert to DataFrame and calculate MAs
        df = util.df(bars)
        df['sma_fast'] = df['close'].rolling(window=5).mean()
        df['sma_slow'] = df['close'].rolling(window=15).mean()

        last = df.iloc[-1]
        prev = df.iloc[-2]

        # Detect crossover
        signal = None
        if prev['sma_fast'] < prev['sma_slow'] and last['sma_fast'] > last['sma_slow']:
            signal = 'BUY'
        elif prev['sma_fast'] > prev['sma_slow'] and last['sma_fast'] < last['sma_slow']:
            signal = 'SELL'

        print(f"📊 Signal: {signal or 'No Signal'}")

        # Place order if signal triggered
        if signal:
            order = MarketOrder(signal, 10)
            trade = ib.placeOrder(contract, order)
            print(f"🚀 Order placed: {signal}")

        print("🛌 Sleeping for 5 minutes...\n")
        time.sleep(300)  # 5 minutes = 300 seconds

except KeyboardInterrupt:
    print("\n🛑 Strategy stopped by user.")

ib.disconnect()
