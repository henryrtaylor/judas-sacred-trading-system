def defer_logic(vote, context, agent_name):
    # Example deferral logic: override vote if certain context is present
    if context.get("volatility") == "High" and agent_name in ["Raphael", "Gabriel"]:
        return "HOLD"  # Silence aggressive agents in high volatility
    if context.get("fomc_day") and agent_name == "Gabriel":
        return "HOLD"  # Gabriel defers on holy days
    return vote
