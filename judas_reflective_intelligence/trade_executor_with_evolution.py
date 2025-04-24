from safe_order import verify_order
from override_check import check_override
from execution_logger import log_execution
from evolve_agent import log_trade_result
from judas_ibkr.safe_order import safe_execute  # guarded limit helper
from ib_insync import IB, Stock, MarketOrder

# -------------------------------------------------------------
# 1. Establish one shared IB connection (paper by default)
# -------------------------------------------------------------
ib = IB()
ib.connect("127.0.0.1", 7497, clientId=6)   # adjust port / id for live

# -------------------------------------------------------------
# 2. Rebalance loop – call after weights are produced
# -------------------------------------------------------------

def rebalance(target_shares: dict[str, float],
              positions: dict[str, float],
              prices_info: dict[str, dict]):
    """Delta‑adjust each symbol using slip‑checked LIMIT orders.

    prices_info must map sym → {"price": float, "guessed": bool}
    """
    for sym, tgt in target_shares.items():
        cur   = positions.get(sym, 0.0)
        delta = tgt - cur
        if abs(delta) < 1e-6:
            continue  # no change

        info = prices_info[sym]
        safe_execute(ib,
                     sym,
                     delta,
                     info["price"],
                     info["guessed"])  # will abort if slip too wide

# -------------------------------------------------------------
# 3. Manual (or strategy) order helper with override + logging
# -------------------------------------------------------------

def execute_order(symbol: str,
                  size: float,
                  side: str,
                  price: float,
                  mode: str = "paper",
                  context: str = "manual",
                  strategy: str = "unknown",
                  confidence: float = 0.0,
                  zion_approved: bool = False) -> bool:
    """One‑off order helper keeping the old logging / override semantics."""
    try:
        verify_order(symbol, size, side, context)

        if not check_override(seconds=7, flag_path="override/stop.txt"):
            print("⛔ Trade override triggered. Execution skipped.")
            return False

        if mode == "live":
            print(f"🚀 LIVE TRADE: {side} {symbol} size={size} @ {price}")
            contract = Stock(symbol.split('-')[0], 'SMART', 'USD')
            order    = MarketOrder(side.upper(), abs(size))
            trade    = ib.placeOrder(contract, order)
            ib.sleep(1.0)  # allow status update
        else:
            print(f"🧪 PAPER TRADE: {side} {symbol} size={size} @ {price}")

        log_execution(symbol, size, side, price, context)
        result = "WIN" if price % 2 == 0 else "LOSS"  # placeholder P/L flag
        log_trade_result(symbol, strategy, confidence, result, zion_approved)
        return True

    except Exception as exc:
        print(f"❌ Trade execution failed: {exc}")
        return False

# -------------------------------------------------------------
# 4. Graceful shutdown helper
# -------------------------------------------------------------

def shutdown_ib():
    if ib.isConnected():
        ib.disconnect()
