"""Light‑weight Polygon adapter used by Judas.

* single request per call by default (``retries`` =1)
* surfaces HTTP‑429 as ``RuntimeError`` so the caller can decide to back‑off
* logs only one concise line per failure attempt

The module **never** sleeps longer than ``RATE_SLEEP`` (250 ms) per attempt so
it tops out around four requests per second – Polygon’s free‑tier limit.
"""
from __future__ import annotations

import logging
import os
import time
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

# ── env / constants ─────────────────────────────────────────────────────────
load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=False)

BASE_URL   = "https://api.polygon.io"
RATE_SLEEP = 0.25                    # ~4 req/sec (free‑tier hard‑limit)
LOGGER     = logging.getLogger(__name__)

# ── helpers ────────────────────────────────────────────────────────────────

def _build_url(symbol: str, start: str, end: str) -> str:
    """Compose the daily‑aggregate endpoint url for *symbol* between two ISO dates."""
    api_key = os.getenv("POLYGON_API_KEY", "")
    return (
        f"{BASE_URL}/v2/aggs/ticker/{symbol}/range/1/day/"
        f"{start}/{end}?limit=50000&apiKey={api_key}"
    )

# ── public helper used by back‑tester ──────────────────────────────────────

def fetch_close(sym: str, day: date) -> dict[str, float]:
    """Return {price, guessed} for *sym* on *day* using get_bars() wrapper."""
    from utils.data_router import get_bars  # imported lazily to avoid cycle

    nxt = day + timedelta(days=1)
    try:
        js = get_bars(sym, start=day.isoformat(), end=nxt.isoformat())
    except RuntimeError as e:            # rate‑limit bubbled up
        LOGGER.warning("rate‑limit on %s: %s", sym, e)
        return {"price": None, "guessed": True}

    if not js or not js.get("results"):
        raise ValueError(f"no bar {sym} {day}")
    rec = js["results"][0]
    price = rec.get("c") or rec.get("Close") or next(iter(rec.values()))
    return {"price": price, "guessed": False}

# ── public api ─────────────────────────────────────────────────────────────

def fetch_polygon(
    symbol: str,
    start: str,
    end: str,
    retries: int = 1,
    *,
    logger: logging.Logger = LOGGER,
) -> Optional[Dict[str, Any]]:
    """Return Polygon *daily* OHLCV JSON or *None* if nothing usable.

    Parameters
    ----------
    symbol   : e.g. ``"SPY"`` or ``"X:BTCUSD"``
    start    : inclusive ISO‑date ``YYYY‑MM‑DD``
    end      : exclusive ISO‑date ``YYYY‑MM‑DD``
    retries  : network retry attempts (default **1**)

    Raises
    ------
    RuntimeError  – propagated on HTTP‑429 so callers can throttle globally.
    """
    if not os.getenv("POLYGON_API_KEY"):
        logger.info("Polygon key missing – skipping %s", symbol)
        return None

    url = _build_url(symbol, start, end)

    for attempt in range(1, retries + 1):
        try:
            time.sleep(RATE_SLEEP)
            resp = requests.get(url, timeout=10)
            if resp.status_code == 429:
                # Let the caller decide how to handle the global rate limit.
                raise RuntimeError("Polygon rate‑limit reached (HTTP 429)")

            resp.raise_for_status()
            data = resp.json()
            if data.get("results"):
                return data

            logger.debug("Polygon returned no results for %s (%s‑%s)", symbol, start, end)
            return None

        except RuntimeError:
            raise  # propagate the 429 so the outer layer can back‑off in bulk
        except Exception as exc:
            logger.debug(
                "Polygon attempt %d/%d failed for %s: %s", attempt, retries, symbol, exc, exc_info=False
            )
            if attempt == retries:
                return None

    return None
