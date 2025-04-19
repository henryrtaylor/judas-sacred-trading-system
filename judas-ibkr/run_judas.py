# run_judas.py
# -*- coding: utf-8 -*-

from divine_filter import reflect_before_trade
from config.settings import WATCHLIST
from signals.signal_engine import generate_signals
from trades.executor import execute_trade
from utils.logger import log_trade
from insight.market_sentiment import get_market_sentiment
from insight.volatility_guard import check_volatility_conditions
from insight.time_windows import get_current_window
from log_to_ledger import log_trade


def run():
    for symbol in WATCHLIST:
        print(f"📡 Scanning {symbol}...")
        df, signal = generate_signals(symbol)
        print(f"📊 Signal for {symbol}: {signal}")
        log_trade(symbol, signal)
        execute_trade(symbol, signal)

if __name__ == "__main__":
    run()
