import numpy as np
from phase15_cap_sym.risk_matrix import build_covariance_matrix

def test_covariance_shape():
    returns = np.random.randn(100, 5)
    cov = build_covariance_matrix(returns)
    assert cov.shape == (5, 5)
