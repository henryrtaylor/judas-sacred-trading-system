# main.py
# -*- coding: utf-8 -*-

from market_data import fetch_market_data
from signal_engine import compute_rsi, compute_moving_averages, compute_macd
from strategy_core import simple_strategy
from trade_executor import execute_trade

def run_judas(symbol="AAPL"):
    print(f"\n📡 Fetching data for: {symbol}")
    df = fetch_market_data(symbol)
    
    df = compute_rsi(df)
    df = compute_moving_averages(df)
    df = compute_macd(df)

    signal = simple_strategy(df)
    print(f"\n📊 Signal for {symbol}: {signal}")
    
    execute_trade(signal, symbol)

if __name__ == "__main__":
    run_judas("AAPL")
