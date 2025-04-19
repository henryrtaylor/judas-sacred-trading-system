import numpy as np
import pandas as pd
from phase15_cap_sym.log_to_sheet import log_to_sheet

def naive_solver(mu, corr, max_weight=0.10):
    inv_corr = np.linalg.pinv(corr)
    raw = inv_corr @ mu.values
    raw = np.maximum(raw, 0)
    w = raw / raw.sum()
    w = np.minimum(w, max_weight)
    w = w / w.sum()
    result = pd.Series(w, index=mu.index)
    for symbol, weight in result.items():
        log_to_sheet("rebalance_logs", action="REBALANCE", symbol=symbol, outcome=weight, notes="naive_solver")
    return result