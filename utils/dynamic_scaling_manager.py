from typing import Dict, List
from .profit_tracker import ProfitTracker
from judas_ibkr.safe_order import safe_execute

class DynamicScalingManager:
    """
    Implements pyramiding/dynamic scaling into winning positions based on profit thresholds.

    thresholds: list of percent gains (e.g., [2.0, 4.0, 6.0])
    scale_fractions: list of fractions of base quantity to add at each threshold (e.g., [0.25, 0.25, 0.5])
    """
    def __init__(
        self,
        profit_tracker: ProfitTracker,
        thresholds: List[float] = None,
        scale_fractions: List[float] = None,
    ):
        self.profit_tracker = profit_tracker
        self.thresholds = thresholds if thresholds is not None else [2.0, 4.0, 6.0]
        self.scale_fractions = scale_fractions if scale_fractions is not None else [0.25, 0.25, 0.5]
        self.scaled_levels: Dict[str, List[bool]] = {}

    def init_symbol(self, symbol: str):
        if symbol not in self.scaled_levels:
            self.scaled_levels[symbol] = [False] * len(self.thresholds)

    def update_and_scale(self, symbol: str, base_qty: float):
        """
        Check profit percent and execute additional orders when thresholds are met.

        :param symbol: Ticker symbol
        :param base_qty: Original position quantity to scale from
        """
        self.init_symbol(symbol)
        current_gain = self.profit_tracker.gain_percent(symbol)
        entry_price = self.profit_tracker.entry_prices.get(symbol)
        if entry_price is None:
            return

        for idx, (thr, frac) in enumerate(zip(self.thresholds, self.scale_fractions)):
            if current_gain >= thr and not self.scaled_levels[symbol][idx]:
                add_qty = base_qty * frac
                print(f"[DynamicScaling] {symbol} at +{current_gain:.2f}% (threshold {thr}%) → scaling +{add_qty}")
                safe_execute(symbol=symbol, side='BUY', quantity=add_qty)
                self.scaled_levels[symbol][idx] = True
