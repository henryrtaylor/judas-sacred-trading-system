"""
utils.guesser
=============

Synthetic price estimator used when all data providers fail.
It keeps a simple exponential‑moving average (EWMA) per symbol and
updates that estimate whenever the *real* bar arrives.

Public API
----------
guess_price(sym)          -> (price: float, guessed: bool=True)
reward_guess(sym, real)   -> None   # feed the real close back
"""

from __future__ import annotations
import math

# hyper‑parameters
_ALPHA    = 0.15        # learning rate: 0.10–0.30 reasonable
_MIN_PX   = 1.0         # never guess below $1

# internal tables
_GUESS: dict[str, float] = {}   # current EWMA guess
_LAST_REAL: dict[str, float] = {}   # last real bar seen


# ----------------------------------------------------------------------
def guess_price(sym: str) -> tuple[float, bool]:
    """
    Return an estimated price and True to flag that it's synthetic.
    If this is the first ever call for `sym`, default to \$100.
    """
    px = _GUESS.get(sym)
    if px is None:
        px = _GUESS[sym] = max(_LAST_REAL.get(sym, 100.0), _MIN_PX)
    return px, True


def reward_guess(sym: str, real: float) -> None:
    """
    Blend the real closing price into the EWMA guess table.
    Call this exactly once each time a true bar is retrieved.
    """
    if real <= 0:
        return
    prev = _GUESS.get(sym, real)
    _GUESS[sym] = prev + _ALPHA * (real - prev)
    _LAST_REAL[sym] = real
