# -------------- alpha_adapter.py --------------
"""Alpha Vantage daily bar fetch (5 calls/min free).
Lazy‑loads ALPHAVANTAGE_API_KEY after dotenv."""
from __future__ import annotations
import os, requests, logging
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
_SESSION = requests.Session()

def fetch_alpha(ticker: str, *, start: str, end: str):
    key = os.getenv("ALPHAVANTAGE_API_KEY", "")
    if not key:
        logging.warning("Alpha key missing")
        return None
    try:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&apikey={key}&outputsize=compact"
        j = _SESSION.get(url, timeout=20).json().get("Time Series (Daily)", {})
        bars = [v for k,v in j.items() if start <= k <= end]
        if not bars:
            return None
        return {"results": bars}
    except Exception as e:
        logging.warning("AlphaVantage fail %s: %s", ticker, e)
    try:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&apikey={KEY}&outputsize=compact"
        j = _SESSION.get(url, timeout=20).json().get("Time Series (Daily)", {})
        bars = [v for k,v in j.items() if start <= k <= end]
        if not bars:
            return None
        return {"results": bars}
    except Exception as e:
        logging.warning("AlphaVantage fail %s: %s", ticker, e)
        return None