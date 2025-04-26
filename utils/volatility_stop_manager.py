from typing import Dict, List
from trade_executor import safe_execute

class VolatilityStopManager:
    """
    Implements ATR-based dynamic trailing stops to adapt to market volatility.

    - atr_window: number of price ticks to compute ATR
    - atr_multiplier: multiplier for ATR to set stop distance
    """
    def __init__(
        self,
        atr_window: int = 14,
        atr_multiplier: float = 2.0,
    ):
        self.atr_window = atr_window
        self.atr_multiplier = atr_multiplier
        # Store price history: list of last N tick prices per symbol
        self.price_history: Dict[str, List[float]] = {}

    def update_price(self, symbol: str, price: float):
        """
        Append the latest price tick to history, trimming to atr_window+1 entries.
        """
        hist = self.price_history.setdefault(symbol, [])
        hist.append(price)
        if len(hist) > self.atr_window + 1:
            hist.pop(0)

    def compute_atr(self, symbol: str) -> float:
        """
        Compute Average True Range using high-low ranges between successive ticks.
        """
        hist = self.price_history.get(symbol, [])
        if len(hist) < 2:
            return 0.0
        # True Range approximated as abs(t_i - t_{i-1})
        tr_list = [abs(curr - prev) for prev, curr in zip(hist, hist[1:])]
        # Only average over last atr_window elements
        tr = tr_list[-self.atr_window:]
        return sum(tr) / len(tr) if tr else 0.0

    def check_and_execute(self, symbol: str, quantity: float):
        """
        If price falls below (current_price - atr_multiplier * ATR), execute sell of quantity.
        """
        hist = self.price_history.get(symbol)
        if not hist:
            return
        current_price = hist[-1]
        atr = self.compute_atr(symbol)
        stop_price = current_price - self.atr_multiplier * atr
        # Trigger sell if price breaches stop level
        if current_price <= stop_price and quantity > 0:
            print(f"[VolatilityStop] {symbol} price {current_price:.2f} <= stop {stop_price:.2f} (ATR {atr:.2f}) → SELL {quantity}")
            safe_execute(symbol=symbol, side='SELL', quantity=quantity)
