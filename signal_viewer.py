
# signal_viewer.py

from tabulate import tabulate

def display_signals(price_data, plugins):
    results = []
    for name, fn in plugins.items():
        try:
            signal_series = fn(price_data)
            latest = signal_series.dropna().iloc[-1]
            interpretation = {
                1: "BUY",
                -1: "SELL",
                0: "NEUTRAL"
            }.get(int(latest), "N/A")
            results.append({
                "Plugin": name,
                "Latest Signal": interpretation
            })
        except Exception as e:
            results.append({
                "Plugin": name,
                "Latest Signal": f"⚠️ ERROR: {str(e)}"
            })

    print("\n📡 Signal Plugin Output:")
    print(tabulate(results, headers="keys", tablefmt="pretty"))
