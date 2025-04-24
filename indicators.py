# indicators.py

import pandas as pd

def get_atr(data, period=14):
    high = data['High']
    low = data['Low']
    close = data['Close']
    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    return atr

def rsi_signal(data: pd.DataFrame, period: int = 14) -> pd.Series:
    delta = data['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / (avg_loss + 1e-9)  # prevent division by zero
    rsi = 100 - (100 / (1 + rs))

    def map_signal(val):
        if val > 70:
            return "SELL"
        elif val < 30:
            return "BUY"
        else:
            return "NEUTRAL"

    return rsi.apply(map_signal)