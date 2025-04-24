from phase16_mosaic.correlation_weave import rolling_corr, load_prices
from phase15_cap_sym.liquidity_oracle import LiquidityOracle
import pandas as pd

def run_risk_matrix():
    print("📊 Rebuilding Quantum‑Risk Matrix...")
    symbols = ["SPY", "BTC-USD", "GLD"]
    try:
        prices = load_prices(symbols)
        corr = rolling_corr(prices, window=30)
        print("✅ Quantum-Risk Matrix built successfully.")
        return True
    except Exception as e:
        print(f"❌ Failed to rebuild Quantum-Risk Matrix: {e}")
        return False

def run_liquidity_oracle():
    print("🔁 Running Liquidity Oracle warm-up...")
    try:
        oracle = LiquidityOracle(["SPY", "BTC-USD", "GLD"])  # fixed positional arg
        oracle.warm_up()
        print("✅ Liquidity Oracle warmed up.")
        return True
    except Exception as e:
        print(f"❌ Liquidity Oracle warm-up failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Judas Warm-Up Sequence...")
    matrix_ready = run_risk_matrix()
    oracle_ready = run_liquidity_oracle()
    if matrix_ready and oracle_ready:
        print("🌟 Judas is fully warmed up and ready.")
    else:
        print("⚠️ Warm-up incomplete. Check logs for details.")