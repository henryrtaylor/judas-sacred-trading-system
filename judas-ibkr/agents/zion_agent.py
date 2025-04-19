from agent_protocol import defer_logic

def evaluate(df, context, agent_name="Zion"):
    vote = "HOLD"  # Placeholder logic
    final_vote = defer_logic(vote, context, agent_name)
    return final_vote
