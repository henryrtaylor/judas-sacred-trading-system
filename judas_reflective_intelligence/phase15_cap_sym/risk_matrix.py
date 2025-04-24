"""Quantum‑Risk Matrix (CPU fallback)

Generates covariance & tail‑risk tensors using quasi‑Monte Carlo.
"""

import numpy as np

def build_covariance_matrix(returns: np.ndarray) -> np.ndarray:
    """Compute covariance matrix of returns (T x N)."""
    return np.cov(returns, rowvar=False)

def monte_carlo_var(returns: np.ndarray, confidence: float = 0.99, sims: int = 10000) -> float:
    samples = np.random.choice(returns.flatten(), (sims, returns.shape[1]))
    pnl = samples.sum(axis=1)
    return float(np.percentile(pnl, (1 - confidence) * 100))
