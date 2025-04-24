# ------------------ judas_reflective_intelligence/rebalance_scheduler_ai.py ----------------
"""AI Portfolio Rebalance Scheduler

Exports
-------
    generate_target_weights(prices, equity, positions) -> dict
        * prices:   dict {symbol: last_close_price}
        * equity:   total portfolio equity (cash + holdings)
        * positions: current shares held {symbol: qty}

Returns a **weight map** where absolute values sum to ≤ 1.  A positive weight
means long exposure; negative weight would be a short (not used here).

The current implementation is very simple:
    • 60‑40 stocks/bonds core using SPY + TLT as proxies
    • 10 % gold hedge (GLD)
    • Remaining 30 % equally split between QQQ, BTC‑USD, ETH‑USD

Feel free to replace with a more sophisticated optimiser (risk‑parity,
mean‑variance, factor tilt, etc.) – just keep the same signature.
"""
from __future__ import annotations
from typing import Dict

CORE = ["SPY", "TLT"]
ALT  = ["QQQ", "BTC-USD", "ETH-USD", "GLD"]

CORE_W = {"SPY": 0.30, "TLT": 0.30}          # 60 % core (60‑40)
ALT_W  = {"QQQ": 0.10, "GLD": 0.10, "BTC-USD": 0.15, "ETH-USD": 0.15}

TARGET_W = {**CORE_W, **ALT_W}

def generate_target_weights(prices: Dict[str,float],
                            equity: float,
                            positions: Dict[str,float]) -> Dict[str,float]:
    """Return static weight map (see docstring).

    The function ignores *prices*, *equity*, and *positions* for now, but the
    signature allows future adaptive logic (volatility targeting, momentum,
    risk guards, etc.).
    """
    # ensure we only output symbols present in prices
    w = {s: wt for s, wt in TARGET_W.items() if s in prices}

    # normalise (should already sum to 1.0 but defensive):
    tot = sum(abs(v) for v in w.values())
    return {s: v / tot for s, v in w.items()}
