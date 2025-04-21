# ------------------ utils/yahoo_adapter.py -------------------
"""Yahoo Finance fallback using yfinance."""
from __future__ import annotations
import logging, datetime as dt
try:
    import yfinance as yf
except ImportError:
    yf = None

def fetch_yahoo(ticker: str, *, start: str, end: str):
    if yf is None:
        logging.warning("yfinance not installed")
        return None
    try:
        df = yf.download(ticker, start=start, end=end, progress=False, interval="1d")
        if df.empty:
            return None
        return {"results": df.to_dict("records")}
    except Exception as e:
        logging.warning("Yahoo fail %s: %s", ticker, e)
        return None