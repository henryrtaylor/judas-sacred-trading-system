
def volatility_multiplier(volatility, sensitivity=1.0):
    return 1 + (volatility * sensitivity)

def adjusted_position_size(position_size, volatility):
    return position_size / volatility_multiplier(volatility)
