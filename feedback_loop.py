
# feedback_loop.py

import json
import yfinance as yf
from datetime import datetime, timedelta

def evaluate_trade_outcome(symbol, entry_price, side, timestamp, lookahead=3):
    try:
        t0 = datetime.fromisoformat(timestamp)
        t1 = t0 + timedelta(days=lookahead)

        df = yf.download(symbol, start=t0.strftime('%Y-%m-%d'), end=t1.strftime('%Y-%m-%d'))
        if df.empty:
            return None

        future_price = df['Close'].iloc[-1]
        if side == 'BUY':
            return round(future_price - entry_price, 2)
        elif side == 'SELL':
            return round(entry_price - future_price, 2)
        else:
            return None
    except:
        return None

def analyze_journal(path='logs/trade_journal.json', lookahead=3):
    with open(path, 'r') as f:
        trades = json.load(f)

    results = []
    for trade in trades:
        result = evaluate_trade_outcome(
            trade['symbol'],
            trade['price'],
            trade['side'],
            trade['timestamp'],
            lookahead
        )
        if result is not None:
            results.append({
                "symbol": trade['symbol'],
                "side": trade['side'],
                "timestamp": trade['timestamp'],
                "entry_price": trade['price'],
                "pnl": result,
                "reason": trade['reason']
            })

    return results
