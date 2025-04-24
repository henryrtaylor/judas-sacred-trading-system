import json
from agents import mathew_agent, gabriel_agent, enoch_agent, sophia_agent, raphael_agent, zion_agent

AGENTS = {
    "Mathew": mathew_agent,
    "Gabriel": gabriel_agent,
    "Enoch": enoch_agent,
    "Sophia": sophia_agent,
    "Raphael": raphael_agent,
    "Zion": zion_agent,
}

def reassess_assets():
    with open('real_portfolio.json', 'r') as f:
        portfolio = json.load(f)

    print("🔍 Reassessing current holdings with divine council...")
    for asset in portfolio:
        symbol = asset['symbol']
        print(f"📈 {symbol} — Agents voting:")

        votes = {}
        for name, agent in AGENTS.items():
            vote = agent.evaluate(df=None, context={"symbol": symbol}, agent_name=name)
            votes[name] = vote
            print(f"  {name}: {vote}")

        consensus = max(set(votes.values()), key=list(votes.values()).count)
        print(f"⚖️ Final Judgment for {symbol}: {consensus}")

if __name__ == "__main__":
    reassess_assets()
