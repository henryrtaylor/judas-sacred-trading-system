
"""Portfolio Solver – Phase 16

A naïve inverse‑covariance optimiser with weight cap fallback.
Swap in D‑Wave or simulated annealing later.
"""

import numpy as np, pandas as pd

def naive_solver(mu: pd.Series, corr: pd.DataFrame, max_weight: float = 0.10) -> pd.Series:
    inv_corr = np.linalg.pinv(corr)
    raw = inv_corr @ mu.values
    raw = np.maximum(raw, 0)            # long‑only
    w = raw / raw.sum()
    w = np.minimum(w, max_weight)       # cap per symbol
    w = w / w.sum()
    return pd.Series(w, index=mu.index)
