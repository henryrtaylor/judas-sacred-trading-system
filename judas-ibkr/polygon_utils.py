
import requests
import pandas as pd
import time
import os

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

def get_polygon_price_data(symbol, timespan="day", multiplier=1, limit=90):
    """
    Fetch OHLCV price data for a symbol from Polygon.io
    """
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/{multiplier}/{timespan}/90d"
    params = {
        "adjusted": "true",
        "sort": "asc",
        "limit": limit,
        "apiKey": POLYGON_API_KEY
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    if "results" not in data:
        raise ValueError(f"No data found for {symbol}")

    df = pd.DataFrame(data["results"])
    df['t'] = pd.to_datetime(df['t'], unit='ms')
    df.set_index('t', inplace=True)
    df.rename(columns={'o': 'open', 'h': 'high', 'l': 'low', 'c': 'close', 'v': 'volume'}, inplace=True)

    return df
