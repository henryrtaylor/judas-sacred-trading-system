import numpy as np

def dynamic_allocation(sentiment_index, base_pct=0.1, sensitivity=0.5, drawdown_factor=0.0):
    raw_alloc = base_pct * (1 + sentiment_index * sensitivity)
    adjusted_alloc = max(0.01, min(0.3, raw_alloc - drawdown_factor))
    return adjusted_alloc

def scale_position(allocation_pct, equity, confidence_score, volatility_multiplier):
    base_position = allocation_pct * equity * confidence_score
    return base_position / volatility_multiplier