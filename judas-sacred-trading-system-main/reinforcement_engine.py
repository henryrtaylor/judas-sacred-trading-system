# reinforcement_engine.py
# 🌱 Sacred Reinforcement Engine — Judas Learns & Adapts

import json
import pandas as pd
from pathlib import Path
from sacred_logger import log_event

# File paths
MEMORY_FILE = "logs/reinforcement_memory.json"
OUTPUT_FILE = "generated/reinforced_preferences.json"

# Load memory log
if not Path(MEMORY_FILE).exists():
    log_event("reinforce", "❌ No memory file found. Skipping RL update.")
    exit()

with open(MEMORY_FILE) as f:
    memory = json.load(f)

if not memory:
    log_event("reinforce", "❌ Memory log is empty.")
    exit()

# Create DataFrame for easier processing
df = pd.DataFrame(memory)

# Default base reward = return_pct + sacred bonus
df['reward'] = df['return_pct']
df['reward'] += df['strategy_tag'].apply(lambda tag: 0.25 if tag in ['golden_cross', 'fib_support'] else 0.0)

# Aggregate by symbol/strategy
grouped = df.groupby(['symbol', 'strategy_tag']).agg(
    avg_reward=('reward', 'mean'),
    trades=('reward', 'count')
).reset_index()

# Normalize reward
max_reward = grouped['avg_reward'].max()
grouped['normalized'] = grouped['avg_reward'] / max_reward

# Create output structure
preferences = {
    row['symbol']: {
        'strategy_tag': row['strategy_tag'],
        'preference_score': round(row['normalized'], 4)
    }
    for _, row in grouped.iterrows()
}

# Save for future use
Path("generated").mkdir(exist_ok=True)
with open(OUTPUT_FILE, "w") as f:
    json.dump(preferences, f, indent=4)

log_event("reinforce", f"✅ Reinforcement updated for {len(preferences)} symbols → {OUTPUT_FILE}")
