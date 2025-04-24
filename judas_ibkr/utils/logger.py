# logger.py
# -*- coding: utf-8 -*-

import datetime

def log_trade(symbol, signal):
    with open("logs/trade_log.txt", "a") as f:
      f.write(f"{datetime.datetime.now()}: {symbol} -> {signal}\n")

