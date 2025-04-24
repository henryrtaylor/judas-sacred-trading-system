import os
import sys
import pandas as pd
from datetime import datetime
import webbrowser

from phase15_cap_sym.solver import naive_solver
from phase15_cap_sym.log_to_sheet import log_to_sheet
from trade_logger import log_trade

def rebalance_now():
    print("🔄 Running rebalance now...")
    symbols = ["SPY", "BTC-USD", "GLD"]
    mu = [0.12, 0.08, 0.05]
    corr = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    weights = naive_solver(
        pd.Series(mu, index=symbols),
        pd.DataFrame(corr, index=symbols, columns=symbols)
    )
    for symbol, weight in weights.items():
        log_trade("paper", symbol, "REBALANCE", weight, "market", "Manual shell rebalance", "Judas", "shell-trigger")
    print("✅ Rebalance complete.")

def log_equity():
    summary = {
        "NetLiquidation": 11042.33,
        "BuyingPower": 8876.45
    }
    log_to_sheet("equity_curve", action="MANUAL", symbol="ACCOUNT", outcome=f"NetLiq={summary['NetLiquidation']}", notes=f"BuyingPower={summary['BuyingPower']}")
    print("✅ Equity logged manually.")

def show_trades(limit=5):
    try:
        df = pd.read_csv("logs/paper_trades.csv")
        print("🧾 Last Trades:")
        print(df.tail(limit).to_string(index=False))
    except Exception as e:
        print(f"❌ Could not read trades: {e}")

def summarize_logs():
    try:
        df = pd.read_csv("logs/paper_trades.csv")
        total = len(df)
        last = df.tail(1)
        print(f"📊 Total Trades: {total}")
        print("🕓 Last Trade:")
        print(last.to_string(index=False))
    except Exception as e:
        print(f"❌ Could not summarize logs: {e}")

def equity_chart():
    try:
        webbrowser.open("http://127.0.0.1:8050")
        print("📈 Equity dashboard opened.")
    except Exception as e:
        print(f"❌ Failed to open dashboard: {e}")

def show_commands():
    print("""
Available Commands:
- rebalance now        → Trigger portfolio rebalance
- log equity           → Log manual equity summary
- show trades          → View last paper trades
- summarize logs       → Count + show last trade
- equity chart         → Open the Plotly Dash equity dashboard
- status               → Agent health check (coming soon)
- speak                → Voice command mode (coming soon)
- archive now          → Trigger IPFS log archive (coming soon)
- reflect now          → Run judgment layer scan (coming soon)
- exit                 → Exit Judas Shell
    """)

def main():
    print("📜 WELCOME TO JUDAS SHELL – Phase 21+")
    print("Type 'help' for a list of commands.")
    while True:
        cmd = input("Judas > ").strip().lower()
        if cmd == "rebalance now":
            rebalance_now()
        elif cmd == "log equity":
            log_equity()
        elif cmd == "show trades":
            show_trades()
        elif cmd == "summarize logs":
            summarize_logs()
        elif cmd == "equity chart":
            equity_chart()
        elif cmd == "help":
            show_commands()
        elif cmd == "exit":
            print("👋 Exiting Judas Shell.")
            break
        else:
            print("❌ Unknown command. Type 'help' for options.")

if __name__ == "__main__":
    main()