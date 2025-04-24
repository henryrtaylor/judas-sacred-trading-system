# signal_engine.py

from market_data import fetch_market_data
from signal_engine import compute_rsi, compute_moving_averages, compute_macd
import pandas as pd

def generate_signals(symbol):
    df = fetch_market_data(symbol)
    df = compute_rsi(df)
    df = compute_moving_averages(df)
    df = compute_macd(df)

    latest = df.iloc[-1]
    if latest["rsi"] < 30 and latest["close"] > latest["sma_long"]:
        return df, "BUY"
    elif latest["rsi"] > 70:
        return df, "SELL"
    else:
        return df, "HOLD"
