from agents.mathew_agent import evaluate as eval_mathew
from agents.gabriel_agent import evaluate as eval_gabriel
from agents.enoch_agent import evaluate as eval_enoch
from agents.sophia_agent import evaluate as eval_sophia
from agents.raphael_agent import evaluate as eval_raphael
from agents.zion_agent import evaluate as eval_zion

def orchestrate_agents(df, context):
    votes = {
        "Mathew": eval_mathew(df, context),
        "Gabriel": eval_gabriel(df, context),
        "Enoch": eval_enoch(df, context),
        "Sophia": eval_sophia(df, context),
        "Raphael": eval_raphael(df, context),
        "Zion": eval_zion(df, context),
    }

    print("\n🧬 Agent Consensus:")
    for agent, vote in votes.items():
        print(f"{agent}: {vote}")

    # Majority vote mechanism
    decisions = list(votes.values())
    final_decision = max(set(decisions), key=decisions.count)

    print(f"⚖️ Judas Final Decision: {final_decision}")
    return final_decision
