
"""Alpha Constellation – Phase 16

Crafts an expected‑return vector from simple factors (momentum + short‑reversal).
Replace with your own factor model when ready.
"""

import pandas as pd, numpy as np

def expected_returns(prices: pd.DataFrame) -> pd.Series:
    momentum = prices.iloc[-1] / prices.iloc[-252] - 1       # 12‑month momentum
    reversal = -(prices.iloc[-1] / prices.iloc[-5] - 1)      # 1‑week reversal
    return 0.7 * momentum + 0.3 * reversal
