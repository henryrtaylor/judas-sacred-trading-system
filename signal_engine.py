# signal_engine.py

import pandas as pd

def get_plugin_signals(df, plugins):
    results = {}
    for plugin_name, plugin_fn in plugins.items():
        try:
            vote_series = plugin_fn(df)
            final_vote = int(vote_series.iloc[-1].item()) if not vote_series.empty else 0
            results[plugin_name] = {
                "series": vote_series,
                "label": "BUY" if final_vote > 0 else "SELL" if final_vote < 0 else "NEUTRAL"
            }
        except Exception as e:
            results[plugin_name] = {"series": pd.Series(dtype=int), "label": f"ERROR: {str(e)}"}
    return results

def compute_consensus(plugin_votes, threshold=2):
    tally = {"BUY": 0, "SELL": 0}
    for result in plugin_votes.values():
        if result["label"] == "BUY":
            tally["BUY"] += 1
        elif result["label"] == "SELL":
            tally["SELL"] += 1
    if tally["BUY"] >= threshold:
        return "BUY"
    elif tally["SELL"] >= threshold:
        return "SELL"
    return "NEUTRAL"