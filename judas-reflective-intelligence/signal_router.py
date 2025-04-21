import random

# Simulated agent signals
def reddit_agent():
    return {'SPY': 0.75, 'BTC-USD': 0.60}

def momentum_agent():
    return {'GLD': 0.85, 'SPY': 0.65}

def macro_agent():
    return {'GLD': 0.80, 'BTC-USD': 0.70}

AGENT_FUNCTIONS = {
    'reddit': reddit_agent,
    'momentum': momentum_agent,
    'macro': macro_agent,
}

def collect_signals():
    votes = {}
    for name, agent_func in AGENT_FUNCTIONS.items():
        signals = agent_func()
        for symbol, confidence in signals.items():
            if symbol not in votes:
                votes[symbol] = {'votes': 0, 'confidence': 0.0}
            votes[symbol]['votes'] += 1
            votes[symbol]['confidence'] += confidence

    # Normalize confidence
    for symbol in votes:
        votes[symbol]['confidence'] = round(votes[symbol]['confidence'] / votes[symbol]['votes'], 4)

    return votes

def rank_signals(votes):
    ranked = sorted(votes.items(), key=lambda x: (x[1]['votes'], x[1]['confidence']), reverse=True)
    return ranked

def run_signal_router():
    print("📡 Running Multi-Agent Signal Council...")
    signals = collect_signals()
    ranked = rank_signals(signals)
    print("🗳️ Council Results:")
    for symbol, data in ranked:
        print(f"{symbol}: {data['votes']} votes | confidence: {data['confidence']}")
    return dict(ranked)

if __name__ == "__main__":
    run_signal_router()