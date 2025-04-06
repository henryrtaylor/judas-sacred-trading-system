import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

data_file = Path("generated/reinforcement_weights.json")

if not data_file.exists():
    print("No reinforcement data found.")
    exit()

df = pd.read_json(data_file).T
df.index = pd.to_datetime(df.index)
df.sort_index(inplace=True)

plt.figure(figsize=(12, 6))
for col in df.columns:
    plt.plot(df.index, df[col], label=col)

plt.title("📈 Reinforcement Weights Over Time")
plt.xlabel("Date")
plt.ylabel("Normalized Weight")
plt.legend()
plt.tight_layout()
plt.grid(True)
plt.show()
