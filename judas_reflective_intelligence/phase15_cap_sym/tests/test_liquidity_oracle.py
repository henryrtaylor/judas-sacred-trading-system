from phase15_cap_sym.liquidity_oracle import LiquidityOracle

def test_slippage():
    oracle = LiquidityOracle('AAPL')
    oracle.update(1_000_000)
    assert oracle.estimate_slippage(5_000) < 0.005
