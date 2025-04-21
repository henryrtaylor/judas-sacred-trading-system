#   • finnhub_adapter.py --------------
"""Daily bar fetch using Finnhub free tier (60 calls/min).
Lazy‑loads FINNHUB_API_KEY so env is read after dotenv."""
from __future__ import annotations
import os, logging, requests, datetime as dt
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
_SESSION = requests.Session()

def fetch_finnhub(ticker: str, *, start: str, end: str):
    key = os.getenv("FINNHUB_API_KEY", "")
    if not key:
        logging.warning("Finnhub key missing")
        return None
    try:
        fr = int(dt.datetime.fromisoformat(start).timestamp())
        to = int(dt.datetime.fromisoformat(end).timestamp())
        url = f"https://finnhub.io/api/v1/stock/candle?symbol={ticker}&resolution=D&from={fr}&to={to}&token={key}"
        j = _SESSION.get(url, timeout=20).json()
        if j.get("s") != "ok":
            return None
        return {"results": list(zip(j["t"], j["c"]))}
    except Exception as e:
        logging.warning("Finnhub fail %s: %s", ticker, e)
        return None
    try:
        fr = int(dt.datetime.fromisoformat(start).timestamp())
        to = int(dt.datetime.fromisoformat(end).timestamp())
        url = f"https://finnhub.io/api/v1/stock/candle?symbol={ticker}&resolution=D&from={fr}&to={to}&token={KEY}"
        j = _SESSION.get(url, timeout=20).json()
        if j.get("s") != "ok":
            return None
        return {"results": list(zip(j["t"], j["c"]))}
    except Exception as e:
        logging.warning("Finnhub fail %s: %s", ticker, e)
        return None
