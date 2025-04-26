# utils/risk_guard_manager.py

from datetime import datetime as dt
from judas_ibkr.safe_order import safe_execute

class RiskGuardManager:
    """
    Enforces absolute risk limits on your portfolio:
     - max_drawdown_pct   : the maximum % drop from peak allowed
     - max_daily_loss_pct : the maximum % drop from start-of-day allowed
    """
    def __init__(self, max_drawdown_pct: float, max_daily_loss_pct: float):
        self.max_drawdown_pct   = max_drawdown_pct
        self.max_daily_loss_pct = max_daily_loss_pct

        # Initialized on first record
        self.start_value = None
        self.peak_value  = None

    def record_portfolio_value(self, current_value: float):
        """
        Call this at the top of each execute() with your total portfolio value.
        - On first call, sets both start_value and peak_value.
        - Thereafter, updates peak_value to the highest seen.
        """
        if self.start_value is None:
            self.start_value = current_value
            self.peak_value  = current_value
        else:
            # Only raise the peak, never lower it
            self.peak_value = max(self.peak_value, current_value)

    def enforce(self, ib, positions: dict[str, float], current_value: float) -> bool:
        """
        Checks current_value against:
         • drawdown = (peak_value - current_value) / peak_value * 100
         • daily loss = (start_value - current_value) / start_value * 100

        If either exceeds its limit, liquidates all open positions via safe_execute
        and returns True (to halt further rebalance). Otherwise returns False.
        """
        # Calculate percentages
        drawdown_pct = (self.peak_value - current_value) / self.peak_value * 100
        daily_loss_pct = (self.start_value - current_value) / self.start_value * 100

        # Check limits
        if drawdown_pct >= self.max_drawdown_pct or daily_loss_pct >= self.max_daily_loss_pct:
            print(f"[RiskGuard] Exceeded risk limits: drawdown {drawdown_pct:.2f}% "
                  f"or daily loss {daily_loss_pct:.2f}%. Liquidating all positions.")
            # Liquidate
            for symbol, qty in positions.items():
                if qty > 0:
                    print(f"[RiskGuard] Liquidating {symbol}: {qty} shares")
                    safe_execute(ib, symbol, -qty, None, False)
            return True

        return False
