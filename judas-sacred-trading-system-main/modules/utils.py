# modules/utils.py

import pandas as pd

def load_historical_prices(filepath='logs/historical_prices.csv'):
    try:
        df = pd.read_csv(filepath)
        df['date'] = pd.to_datetime(df['date'])
        return df
    except Exception as e:
        print(f"[⚠️] Failed to load historical prices: {e}")
        return pd.DataFrame()

def clean_price_data(df_symbol):
    df_symbol = df_symbol.copy()
    df_symbol = df_symbol[df_symbol['close'].notnull()]
    df_symbol = df_symbol.sort_values(by='date')
    df_symbol = df_symbol.reset_index(drop=True)
    return df_symbol if len(df_symbol) >= 10 else None
