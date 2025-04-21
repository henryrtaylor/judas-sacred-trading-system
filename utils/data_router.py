# ------------------ utils/data_router.py --------------------
"""Provider‑agnostic get_bars with round‑robin equity routing
and Polygon‑only crypto."""
from __future__ import annotations
import itertools, logging
from datetime import date as _date
from utils.polygon_adapter import fetch_polygon
from utils.finnhub_adapter import fetch_finnhub
from utils.alpha_adapter import fetch_alpha
from utils.yahoo_adapter import fetch_yahoo

_PROVIDERS_EQUITY = [fetch_finnhub, fetch_alpha, fetch_yahoo, fetch_polygon]
_provider_cycle = itertools.cycle(_PROVIDERS_EQUITY)


def _norm(sym: str) -> str:
    return sym.upper()


def get_bars(ticker: str, *, start: str | None = None, end: str | None = None):
    """Unified daily bar fetch.

    For equities/ETFs: Finnhub → Alpha → Yahoo → Polygon.
    For crypto (identified by X: prefix or -USD suffix): Polygon only.
    """
    start = start or _date.today().isoformat()
    end = end or start
    sym = _norm(ticker)

    # ---- crypto shortcut -----------------------------------
    if sym.endswith("-USD") or sym.startswith("X:"):
        symbol = sym if sym.startswith("X:") else "X:" + sym.replace("-USD", "USD")
        return fetch_polygon(symbol, start, end)

    # ---- equity round‑robin --------------------------------
    tried = []
    for _ in range(len(_PROVIDERS_EQUITY)):
        provider = next(_provider_cycle)
        tried.append(provider.__name__)
        js = provider(sym, start=start, end=end)
        if js:
            return js
    logging.warning("All providers failed for %s (%s)", sym, ", ".join(tried))
    return None
