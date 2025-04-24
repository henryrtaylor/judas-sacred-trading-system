# ------------------ utils/data_router.py --------------------
"""Unified bar fetcher that fans out across multiple free providers.
   get_bars(symbol, start, end) -> JSON dict or None

   • Equities/ETFs:  round‑robin Finnhub → Alpha Vantage → Yahoo Finance → Polygon
   • Crypto (…‑USD or X: prefix): Polygon only
"""
from __future__ import annotations

import itertools, logging
from typing import Optional, Dict, Any

from utils.polygon_adapter import fetch_polygon
from utils.finnhub_adapter  import fetch_finnhub
from utils.alpha_adapter    import fetch_alpha
from utils.yahoo_adapter    import fetch_yahoo
from utils.guesser import guess_price, reward_guess


# providers for equities in fail‑over order
_EQUITY_PROVIDERS = [fetch_finnhub, fetch_alpha, fetch_yahoo, fetch_polygon]
_cycle = itertools.cycle(_EQUITY_PROVIDERS)

# ----------------------------------------------------------------------

def _is_crypto(sym: str) -> bool:
    return sym.upper().endswith("-USD") or sym.upper().startswith("X:")


def get_bars(symbol: str, *, start: str, end: str) -> Optional[Dict[str, Any]]:
    """Return OHLCV JSON for [start, end) or None if every provider fails."""

    sym = symbol.upper()

    # ---- crypto goes straight to Polygon --------------------------------
    if _is_crypto(sym):
        pol = sym if sym.startswith("X:") else "X:" + sym.replace("-USD", "USD")
        return fetch_polygon(pol, start, end)

    # ---- equities/ETFs ---------------------------------------------------
    tried = []
    for _ in range(len(_EQUITY_PROVIDERS)):
        provider = next(_cycle)
        tried.append(provider.__name__)
        try:
            js = provider(sym, start=start, end=end)
        except Exception as exc:
            logging.warning("%s provider %s failed: %s", sym, provider.__name__, exc)
            js = None
        if js and js.get("results"):
            return js
    logging.warning("All providers failed for %s (%s)", sym, ", ".join(tried))
    return None
