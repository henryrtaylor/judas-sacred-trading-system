from phase15_cap_sym.solver import naive_solver
from trade_logger import log_trade
from phase15_cap_sym.log_to_sheet import log_to_sheet
import pandas as pd
import numpy as np
from datetime import datetime

symbols = ["SPY", "BTC-USD", "GLD"]
mu = pd.Series([0.12, 0.08, 0.05], index=symbols)
corr = pd.DataFrame(np.identity(len(symbols)), index=symbols, columns=symbols)

def simulate_prices():
    return mu, corr

def simulate_allocation_and_log():
    mu, corr = simulate_prices()
    weights = naive_solver(mu, corr)
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    print(f"🧠 {timestamp} – Rebalance weights:")
    print(weights)

    for symbol, weight in weights.items():
        log_trade(
            mode="paper",
            symbol=symbol,
            action="REBALANCE",
            size=weight,
            price="market",
            reason="Daily scheduled rebalance",
            notes="auto-rebalance"
        )

if __name__ == "__main__":
    print("🔄 Starting daily rebalance...")
    simulate_allocation_and_log()
    print("✅ Rebalance complete and logged.")