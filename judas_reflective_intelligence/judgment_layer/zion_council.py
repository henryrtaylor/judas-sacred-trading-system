from datetime import datetime
import random

class ZionCouncil:
    def __init__(self):
        self.agents = [
            "Zion", "Mara", "Asher", "Veda", "Thalos", "Ayra", "Kether"
        ]
        self.symbols = {
            "Zion": "🔥", "Mara": "🌊", "Asher": "⚔️", "Veda": "🌀",
            "Thalos": "🧱", "Ayra": "🌿", "Kether": "🔮"
        }

    def reflect(self, context):
        score = 0
        votes = {}
        for agent in self.agents:
            strength = random.uniform(0.5, 1.0) if random.random() > 0.1 else random.uniform(0.0, 0.4)
            votes[agent] = strength
            score += strength

        avg_score = round((score / len(self.agents)) * 100, 2)
        recommendation = "YES" if avg_score >= 60 else "NO"

        response = {
            "timestamp": datetime.utcnow().isoformat(),
            "context": context,
            "votes": {agent: f"{self.symbols[agent]} {'Strong' if votes[agent] > 0.6 else 'Low'} ({votes[agent]:.2f})" for agent in self.agents},
            "alignment_score": avg_score,
            "consensus": f"Proceed = {recommendation}"
        }
        return response

if __name__ == "__main__":
    council = ZionCouncil()
    result = council.reflect("Simulated Rebalance BTC-USD")
    for k, v in result["votes"].items():
        print(f"{k}: {v}")
    print(f"Score: {result['alignment_score']} | {result['consensus']}")