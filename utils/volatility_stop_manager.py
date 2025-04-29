# utils/volatility_stop_manager.py

from judas_ibkr.safe_order import safe_execute

class VolatilityStopManager:
    """
    Implements ATR-based dynamic trailing stops to adapt to market volatility.

    - atr_window: number of price ticks to compute ATR
    - atr_multiplier: multiplier for ATR to set stop distance
    """
    def __init__(
        self,
        ib,
        atr_window: int = 14,
        atr_multiplier: float = 2.0,
    ):
        self.ib = ib
        self.atr_window = atr_window
        self.atr_multiplier = atr_multiplier
        # Store price history: list of last N tick prices per symbol
        self.price_history = {}

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
        Compute Average True Range approximated from tick-to-tick moves.
        """
        hist = self.price_history.get(symbol, [])
        if len(hist) < 2:
            return 0.0
        tr_list = [abs(curr - prev) for prev, curr in zip(hist, hist[1:])]
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
        if current_price <= stop_price and quantity > 0:
            print(f"[VolatilityStop] {symbol} price {current_price:.2f} <= stop {stop_price:.2f} (ATR {atr:.2f}) → SELL {quantity}")
            safe_execute(self.ib, symbol, -quantity, None, False)
