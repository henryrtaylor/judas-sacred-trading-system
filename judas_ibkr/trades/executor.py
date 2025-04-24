# executor.py

from config.settings import PAPER_MODE, MAX_POSITION_SIZE

def execute_trade(symbol, signal):
    print(f"Executing {signal} for {symbol} (Paper: {PAPER_MODE})")
    # Placeholder logic for paper/live trade
