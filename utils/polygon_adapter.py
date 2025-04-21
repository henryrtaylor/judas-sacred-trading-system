# -------------- utils/polygon_adapter.py --------------
from __future__ import annotations
import logging, os, time, requests
from datetime import datetime as _dt
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv
# Load keys at call‑time so apiKey is never blank
load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=False)

_BASE = "https://api.polygon.io"
_RATE_SLEEP = 0.25  # 4 req/sec


def _build_url(sym: str, start: str, end: str) -> str:
    key = os.getenv("POLYGON_API_KEY", "")
    return f"{_BASE}/v2/aggs/ticker/{sym}/range/1/day/{start}/{end}?limit=50000&apiKey={key}"


def fetch_polygon(sym: str, start: str, end: str, max_tries: int = 3) -> Dict[str, Any] | None:
    """Return Polygon daily‑agg json or None. Works for equities & crypto."""
    if not os.getenv("POLYGON_API_KEY"):
        logging.warning("Polygon key missing ‑ skipping %s", sym)
        return None

    url = _build_url(sym, start, end)
    for attempt in range(1, max_tries + 1):
        try:
            time.sleep(_RATE_SLEEP)
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            js = r.json()
            if js.get("results"):
                return js
            logging.warning("Polygon returned empty results (%s)", sym)
            return None
        except Exception as exc:
            logging.warning("Polygon fail %s attempt %d: %s", sym, attempt, exc)
    return None