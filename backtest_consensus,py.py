
# backtest_consensus.py

import pandas as pd
from signal_engine import get_plugin_signals, compute_consensus
from trade_logger import TradeLogger
from performance_logger import PerformanceLogger

def backtest_consensus(price_data_by_symbol, config, threshold=2):
    logger = TradeLogger(log_path='logs/backtest_journal.json')
    perf_logger = PerformanceLogger(log_path='logs/backtest_performance.json')

    equity = 100000
    position_size = 1000  # fixed trade per consensus trigger
    history = []

    for symbol, df in price_data_by_symbol.items():
        signals = get_plugin_signals(df, config["plugins"])
        df["consensus"] = [compute_consensus(get_plugin_signals(df.iloc[:i+1], config["plugins"]), threshold)
                           if i >= threshold else "NEUTRAL"
                           for i in range(len(df))]

        for i, row in df.iterrows():
            decision = row["consensus"]
            price = row["Close"]
            if decision in ["BUY", "SELL"]:
                qty = position_size // price
                side = decision
                reason = f"Backtest {decision} at {price}"
                logger.log_trade(symbol, side, qty, price, reason)
                perf_logger.log_run(symbol, decision, {k: v['label'] for k, v in signals.items()}, 1)
                equity += qty * price * (1 if side == "SELL" else -1)
                history.append(equity)

    return pd.Series(history)
