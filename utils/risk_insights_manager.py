import logging
from datetime import datetime
from typing import Dict, List, Optional

class RiskInsightsManager:
    """
    Gathers and reports key portfolio risk/return analytics:
      - Running drawdown series
      - Realized / unrealized P&L
      - Win/Loss trade counts
      - Volatility metrics (e.g., rolling std dev)
      - Alerts on threshold breaches via logging or external hooks
    """
    def __init__(
        self,
        alert_thresholds: Optional[Dict[str, float]] = None,
        rolling_window: int = 20,
    ):
        # alert_thresholds: {'drawdown':5.0, 'volatility':2.0, ...}
        self.alert_thresholds = alert_thresholds or {}
        self.rolling_window = rolling_window
        # Historic series for metrics
        self.equity_curve: List[float] = []
        self.trade_results: List[float] = []
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('RiskInsights')

    def record_equity(self, value: float):
        """Call each cycle with current portfolio equity value"""
        self.equity_curve.append(value)
        # Maintain rolling window
        if len(self.equity_curve) > self.rolling_window:
            self.equity_curve.pop(0)

    def record_trade(self, pnl: float):
        """Record realized P&L for a completed trade"""
        self.trade_results.append(pnl)
        self.logger.info(f"Trade recorded: P&L={pnl:.2f}")

    def compute_drawdown(self) -> float:
        """Return max drawdown from recorded equity curve"""
        max_val = max(self.equity_curve, default=0)
        cur_val = self.equity_curve[-1] if self.equity_curve else 0
        if max_val <= 0:
            return 0.0
        return (max_val - cur_val) / max_val * 100

    def compute_volatility(self) -> float:
        """Return rolling volatility (std dev) of equity changes"""
        if len(self.equity_curve) < 2:
            return 0.0
        # simple std dev of returns
        returns = [
            (self.equity_curve[i] - self.equity_curve[i-1]) / self.equity_curve[i-1]
            for i in range(1, len(self.equity_curve)) if self.equity_curve[i-1] != 0
        ]
        mean = sum(returns) / len(returns)
        var = sum((r - mean)**2 for r in returns) / len(returns)
        return var**0.5 * (252**0.5)  # annualize assuming daily data

    def check_alerts(self):
        """Compare metrics to thresholds and log alerts"""
        drawdown = self.compute_drawdown()
        volatility = self.compute_volatility()
        now = datetime.utcnow().isoformat()

        if 'drawdown' in self.alert_thresholds and drawdown >= self.alert_thresholds['drawdown']:
            self.logger.warning(f"[{now}] ALERT: Drawdown {drawdown:.2f}% ≥ threshold {self.alert_thresholds['drawdown']}%")
        if 'volatility' in self.alert_thresholds and volatility >= self.alert_thresholds['volatility']:
            self.logger.warning(f"[{now}] ALERT: Volatility {volatility:.2f} ≥ threshold {self.alert_thresholds['volatility']}")

    def summary(self) -> Dict[str, float]:
        """Return a summary of current risk metrics"""
        return {
            'drawdown_pct': self.compute_drawdown(),
            'volatility': self.compute_volatility(),
            'trades': len(self.trade_results),
            'average_trade_pnl': sum(self.trade_results)/len(self.trade_results) if self.trade_results else 0.0,
        }
