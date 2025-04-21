# -------------- utils/data_router.py --------------
from __future__ import annotations
import logging, os
from pathlib import Path
from datetime import datetime as _dt
from typing import Any, Dict, Callable, List

from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env", override=False)

# —––– INDIVIDUAL PROVIDERS ––––
from .finnhub_adapter    import fetch_finnhub    # type: ignore
from .alpha_adapter      import fetch_alpha      # type: ignore
from .yahoo_adapter      import fetch_yahoo      # type: ignore
from .polygon_adapter    import fetch_polygon    # type: ignore

# Try equities with Finnhub ➜ Alpha ➜ Yahoo first, Polygon last (crypto goes Polygon only)
_PROVIDERS: List[Callable[[str,str,str], Dict[str,Any] | None]] = [
    fetch_finnhub,
    fetch_alpha,
    fetch_yahoo,
    fetch_polygon
]

def _norm(ticker: str) -> str:
    """
    • Upper‑cases equities.
    • Converts 'BTC-USD' ➜ 'X:BTCUSD', 'ETH-USD' ➜ 'X:ETHUSD' for Polygon.
    """
    up = ticker.upper()
    if up.endswith("-USD"):
        return "X:" + up.replace("-", "")
    return up

# --------------------------------------------------
def get_bars(ticker: str, start: str, end: str) -> Dict[str, Any] | None:
    """
    • Crypto symbols (‑USD) go straight to Polygon.
    • Equities/ETFs try Finnhub → Alpha → Yahoo → Polygon.
    """
    sym = _norm(ticker)

    # --- crypto shortcut --------------------------------------------------
    if sym.startswith("X:"):                       # BTC‑USD → X:BTCUSD
        return fetch_polygon(sym, start=start, end=end)

    # --- equities round‑robin ---------------------------------------------
    for fetch in _PROVIDERS:                       # finnhub ➜ alpha ➜ yahoo ➜ polygon
        try:
            js = fetch(sym, start=start, end=end)  # keyword args keep signatures happy
            if js and js.get("results"):
                logging.info("%s fetched via %s (%d bars)",
                             ticker, fetch.__name__, len(js['results']))
                return js
        except Exception as exc:
            logging.warning("%s provider %s failed: %s", ticker, fetch.__name__, exc)

    logging.error("All providers failed for %s", ticker)
    return None

    """
    Round‑robin through providers until one returns JSON with 'results'.
    """
    sym = _norm(ticker)
    for fetch in _PROVIDERS:
        try:
            js = fetch(sym, start=start, end=end)

            if js and js.get("results"):
                logging.info("%s fetched via %s (%d bars)", ticker, fetch.__name__, len(js["results"]))
                return js
        except Exception as exc:
            logging.warning("%s provider %s failed: %s", ticker, fetch.__name__, exc)
    logging.error("All providers failed for %s", ticker)
    return None
# -------------- end utils/data_router.py ----------
