import json
from datetime import datetime as dt

from judas_ibkr.safe_order import safe_execute as _safe_execute
from utils.broker_adapter import fetch_ibkr_state
from judas_reflective_intelligence.rebalance_scheduler_ai import generate_target_weights

from utils.profit_tracker import ProfitTracker
from utils.take_profit_manager import TakeProfitManager
from utils.dynamic_scaling_manager import DynamicScalingManager
from utils.trailing_stop_manager import TrailingStopManager
from utils.risk_guard_manager import RiskGuardManager
from utils.volatility_stop_manager import VolatilityStopManager
from utils.position_sizer_manager import PositionSizerManager
from utils.risk_insights_manager import RiskInsightsManager

class Rebalancer:
    def __init__(
        self,
        watch_list: list[str],
        leverage: float,
        threshold: float,
        max_trade_fraction: float,
        min_price_points: int,
        ib,  # your IB connection instance
    ):
        self.watch_list = watch_list
        self.leverage = leverage
        self.threshold = threshold
        self.max_trade_fraction = max_trade_fraction
        self.min_price_points = min_price_points
        self.ib = ib
        self.prices = {s: None for s in watch_list}
        self.last_rebalance_time = dt.utcnow()

        # Make safe_execute overrideable per instance
        self.safe_execute = _safe_execute

        # Phase 2: Profit & Scaling
        self.profit_tracker = ProfitTracker()
        self.take_profit_mgr = TakeProfitManager(self.profit_tracker)
        self.scaler = DynamicScalingManager(self.profit_tracker)
        # Phase 3: Trailing Stop & Risk Guard
        self.trailing_stop_mgr = TrailingStopManager(self.ib, self.profit_tracker, drawdown_pct=3.0)
        self.risk_guard = RiskGuardManager(max_drawdown_pct=5.0, max_daily_loss_pct=2.0)
        # Phase 4: Volatility Stop
        self.vol_stop_mgr = VolatilityStopManager(self.ib, atr_window=14, atr_multiplier=2.0)
        # Phase 5: Position Sizing
        self.pos_sizer_mgr = PositionSizerManager(
            risk_per_trade_pct=1.0,
            volatility_mgr=self.vol_stop_mgr,
            trailing_mgr=self.trailing_stop_mgr
        )
        # Celestial Risk Insights
        self.risk_insights = RiskInsightsManager(
            alert_thresholds={'drawdown': 5.0, 'volatility': 0.02},
            rolling_window=20
        )

    def update_price(self, symbol: str, price: float):
        self.prices[symbol] = price
        self.profit_tracker.update_price(symbol, price)
        self.trailing_stop_mgr.update_price(symbol, price)
        self.vol_stop_mgr.update_price(symbol, price)

    def should_rebalance(self, now=None):
        now = now or dt.utcnow()
        elapsed = (now - self.last_rebalance_time).total_seconds()
        return elapsed >= self.min_price_points and all(self.prices.values())

    async def execute(self):
        result = await fetch_ibkr_state(self.ib)
        if isinstance(result, tuple) and len(result) == 2:
            cash, positions = result
        else:
            cash = result
            positions = {}

        total_value = cash + sum(self.prices[s] * positions.get(s, 0) for s in self.watch_list)

        # Record equity for insights
        self.risk_insights.record_equity(total_value)

        # Enforce risk guard
        self.risk_guard.record_portfolio_value(total_value)
        if self.risk_guard.enforce(self.ib, positions, total_value):
            self.risk_insights.check_alerts()
            self.last_rebalance_time = dt.utcnow()
            return

        # Compute target weights
        target_weights = generate_target_weights(self.prices, total_value, positions)

        # Rebalance with position sizing
        for sym, w in target_weights.items():
            price_ref = self.prices[sym]
            weight_qty = int(w * total_value / price_ref)
            risk_qty = self.pos_sizer_mgr.size_position(sym, price_ref, total_value)
            desired_qty = weight_qty if risk_qty <= 0 else min(weight_qty, risk_qty)
            current_qty = positions.get(sym, 0)
            delta = desired_qty - current_qty

            side = 'BUY' if delta > 0 else 'SELL'
            print(f"[{dt.utcnow()}] [trade] {side} {abs(delta)} {sym}")
            self.safe_execute(self.ib, sym, delta, price_ref, False)
            if delta > 0:
                self.profit_tracker.update_entry(sym, price_ref)

        # Take-Profit
        for sym in self.watch_list:
            self.take_profit_mgr.check_and_execute(sym)

        # Dynamic Scaling
        for sym in self.watch_list:
            qty = positions.get(sym, 0)
            if qty > 0:
                self.scaler.update_and_scale(sym, qty)

        # Trailing Stop
        for sym in self.watch_list:
            qty = positions.get(sym, 0)
            if qty > 0:
                self.trailing_stop_mgr.check_and_execute(sym, qty)

        # Volatility Stop
        for sym in self.watch_list:
            qty = positions.get(sym, 0)
            if qty > 0:
                self.vol_stop_mgr.check_and_execute(sym, qty)

        # Final alert check
        self.risk_insights.check_alerts()
        self.last_rebalance_time = dt.utcnow()

    async def stream_and_rebalance(self, ps):
        msg = await ps.get_message(ignore_subscribe_messages=True, timeout=1.0)
        if msg and msg['type'] == 'message':
            payload = json.loads(msg['data'])
            print(f"[{dt.utcnow()}] Tick → {payload['s']} @ {payload['p']}")
            self.update_price(payload['s'], payload['p'])
        if self.should_rebalance(now=dt.utcnow()):
            print(f"[{dt.utcnow()}] → Rebalance triggered")
            await self.execute()
