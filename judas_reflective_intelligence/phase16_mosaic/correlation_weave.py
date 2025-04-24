
"""Correlation Weave – Phase 16

Generates rolling correlation matrices (30, 90, 252 trading‑day windows).

Placeholder `load_prices` returns random‑walk data; swap in IBKR historical pulls.

Usage:
    python correlation_weave.py --symbols AAPL SPY MSFT
"""

import argparse, logging, numpy as np, pandas as pd
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s", datefmt="%H:%M:%S")

def load_prices(symbols):
    # TODO → replace with real price loader (IBKR or your cache)
    idx = pd.date_range(end=pd.Timestamp.today(), periods=252)
    rng = np.random.default_rng(seed=42)
    data = {s: 100 + np.cumsum(rng.standard_normal(len(idx))) for s in symbols}
    return pd.DataFrame(data, index=idx)

def rolling_corr(df, window):
    pct = df.pct_change()
    return pct.rolling(window).corr()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--symbols', nargs='+', required=True)
    ap.add_argument('--windows', nargs='+', type=int, default=[30,90,252])
    args = ap.parse_args()

    prices = load_prices(args.symbols)
    out = Path('data/correlation')
    out.mkdir(parents=True, exist_ok=True)

    for w in args.windows:
        rho = rolling_corr(prices, w).dropna()
        file = out / f'rho_{w}.parquet'
        rho.to_parquet(file)
        logging.info("Saved %s", file)

if __name__ == '__main__':
    main()
