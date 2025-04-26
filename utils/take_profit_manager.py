from typing import Optional
from .profit_tracker import ProfitTracker
from trade_executor import safe_execute

class TakeProfitManager:
    """
    Manager to evaluate profit targets and execute take-profit orders when thresholds are met.
    """
    def __init__(self, profit_tracker: ProfitTracker, default_target_pct: float = 7.0):
        self.profit_tracker = profit_tracker
        self.default_target_pct = default_target_pct

    def check_and_execute(self, symbol: str, quantity: Optional[float] = None, target_pct: Optional[float] = None):
        """
        Check if symbol has reached the take-profit threshold and execute a sell order.

        :param symbol: The ticker symbol to monitor
        :param quantity: Number of shares/contracts to sell. If None, will attempt to fetch full position.
        :param target_pct: Profit percentage threshold. If None, uses default_target_pct.
        """
        pct = target_pct if target_pct is not None else self.default_target_pct
        if self.profit_tracker.needs_take_profit(symbol, pct):
            # Determine quantity
            if quantity is None:
                try:
                    from portfolio import get_position  # placeholder import
                    quantity = get_position(symbol)
                except ImportError:
                    raise ValueError("Quantity not specified and get_position not available")

            if quantity and quantity > 0:
                # Execute a safe sell order
                print(f"[TakeProfitManager] Executing take-profit for {symbol}, qty={quantity}")
                safe_execute(symbol=symbol, side='SELL', quantity=quantity)
            else:
                print(f"[TakeProfitManager] No position quantity available for {symbol}")
