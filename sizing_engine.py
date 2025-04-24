# sizing_engine.py

from datetime import datetime

def baseline_allocation(equity, sentiment_index, base_pct=0.02, sensitivity=0.5, drawdown_pct=0.0, drawdown_threshold=0.1):
    adjusted_pct = base_pct * (1 + sentiment_index * sensitivity)
    if drawdown_pct > drawdown_threshold:
        adjusted_pct *= 0.5  # Drawdown safety trigger
    adjusted_pct = max(0.01, min(adjusted_pct, 0.5))  # Clamp between 1% and 50%
    return equity * adjusted_pct

def adjust_for_confidence(position_size, confidence_score):
    return position_size * confidence_score

def adjust_for_volatility(position_size, volatility, sensitivity=1.0):
    if volatility == 0:
        return position_size
    return position_size / (volatility * sensitivity)

def fixed_lot_with_flow(base_lot, portfolio_risk_pct, max_risk=0.2):
    risk_factor = max(0.1, 1 - (portfolio_risk_pct / max_risk))
    return base_lot * risk_factor

def manual_override(original_size, user_input, reason=""):
    override_log = {
        "timestamp": datetime.utcnow().isoformat(),
        "original_size": original_size,
        "user_input": user_input,
        "reason": reason
    }
    # This could be logged to a file or database in a full system
    print("🧠 Manual Override:", override_log)
    return user_input

def calculate_position_size(
    equity,
    sentiment_index,
    confidence_score,
    volatility,
    drawdown_pct=0.0,
    base_pct=0.02,
    sensitivity=0.5,
    volatility_sensitivity=1.0,
    drawdown_threshold=0.1
):
    base_alloc = baseline_allocation(
        equity, sentiment_index, base_pct, sensitivity, drawdown_pct, drawdown_threshold
    )
    sized_by_conf = adjust_for_confidence(base_alloc, confidence_score)
    final_size = adjust_for_volatility(sized_by_conf, volatility, volatility_sensitivity)
    return round(final_size, 2)