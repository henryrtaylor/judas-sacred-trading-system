from log_to_sheet import log_to_sheet

def calculate_position_size(capital: float, risk_perc: float, stop_distance: float) -> int:
    if stop_distance <= 0:
        raise ValueError("stop_distance must be > 0")
    dollar_risk = capital * risk_perc
    shares = dollar_risk / stop_distance
    return int(max(shares, 0))

def apply_drawdown_guardrail(size: int, max_drawdown_flag: bool) -> int:
    return 0 if max_drawdown_flag else size

def check_leverage_and_margin(notional, net_liq, margin_ratio):
    gross_leverage = notional / net_liq
    if gross_leverage > 2.0:
        log_to_sheet("risk_alerts", action="LEVERAGE", outcome=gross_leverage, notes="scaled down >2x")
    if margin_ratio > 0.8:
        log_to_sheet("risk_alerts", action="MARGIN", outcome=margin_ratio, notes="high usage")