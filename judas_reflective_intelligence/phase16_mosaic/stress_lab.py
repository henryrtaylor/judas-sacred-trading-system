
"""Stress Lab – Phase 16

Framework to apply predefined shock vectors to expected returns.
"""

import pandas as pd

def apply_shock(mu: pd.Series, shock_vector: pd.Series) -> pd.Series:
    return mu.add(shock_vector, fill_value=0)
