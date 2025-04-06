
def validate_micro_signal(signal):
    if signal['confidence'] > 0.7 and signal['volatility'] < 2.0:
        return True
    return False
