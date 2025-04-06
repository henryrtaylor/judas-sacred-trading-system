
import numpy as np

def dynamic_allocation(sentiment_index, base_pct=0.05, sensitivity=0.8, floor=0.01, ceiling=0.2, drawdown_factor=0):
    allocation = base_pct * (1 + sentiment_index * sensitivity)
    allocation *= (1 - drawdown_factor)
    return max(floor, min(allocation, ceiling))
