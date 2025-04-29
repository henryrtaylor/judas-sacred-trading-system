from typing import Optional
from utils.volatility_stop_manager import VolatilityStopManager
from utils.trailing_stop_manager import TrailingStopManager

class PositionSizerManager:
    """
    Calculates optimal position sizes per trade based on your risk budget.

    - risk_per_trade_pct: percentage of total capital you're willing to risk per trade (e.g., 1.0 for 1%).
    - Uses volatility (ATR) or trailing stop distance for risk denominator.
    """
    def __init__(
        self,
        risk_per_trade_pct: float = 1.0,
        volatility_mgr: Optional[VolatilityStopManager] = None,
        trailing_mgr: Optional[TrailingStopManager] = None,
    ):
        self.risk_per_trade_pct = risk_per_trade_pct
        self.volatility_mgr = volatility_mgr
        self.trailing_mgr = trailing_mgr

    def size_position(self, symbol: str, price: float, total_value: float) -> int:
        """
        Determine position size such that max risk = risk_per_trade_pct * total_value.

        Attempts to use volatility-based stop (atr * atr_multiplier).
        Falls back to trailing stop distance if volatility not available.
        """
        # Risk budget in dollars
        risk_amount = total_value * (self.risk_per_trade_pct / 100)

        # Determine stop distance
        stop_distance = None
        if self.volatility_mgr:
            atr = self.volatility_mgr.compute_atr(symbol)
            if atr and self.volatility_mgr.atr_multiplier:
                stop_distance = atr * self.volatility_mgr.atr_multiplier
        if stop_distance is None and self.trailing_mgr:
            peak = self.trailing_mgr.peak_prices.get(symbol)
            current = self.trailing_mgr.profit_tracker.current_prices.get(symbol)
            if peak and current:
                stop_distance = peak * (self.trailing_mgr.drawdown_pct / 100)

        # If no valid stop distance, return zero size
        if not stop_distance or stop_distance <= 0:
            return 0

        # Calculate quantity based on risk amount
        qty = int(risk_amount / stop_distance)
        return max(qty, 0)
