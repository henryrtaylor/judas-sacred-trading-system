import random

# Simulate volatility check from VIX or macro index data
def check_volatility_conditions():
    states = ["Calm", "Moderate", "High Volatility"]
    condition = random.choice(states)
    print(f"⚠️ Volatility State: {condition}")
    return condition
