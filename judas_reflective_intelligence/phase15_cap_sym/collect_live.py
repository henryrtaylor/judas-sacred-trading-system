from ib_insync import IB
from log_to_sheet import log_to_sheet
import os
from datetime import datetime
import csv

def get_ibkr_equity_summary():
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)
    account_summary = ib.accountSummary()
    values = {item.tag: float(item.value) for item in account_summary if item.tag in ["NetLiquidation", "BuyingPower"]}
    ib.disconnect()
    return {
        "NetLiquidation": values.get("NetLiquidation", 0.0),
        "BuyingPower": values.get("BuyingPower", 0.0)
    }

def log_equity_update(summary):
    netliq = summary.get("NetLiquidation")
    buying = summary.get("BuyingPower")
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    # Log to Google Sheet
    log_to_sheet("equity_curve", action="UPDATE", symbol="ACCOUNT", outcome=f"NetLiq={netliq}", notes=f"BuyingPower={buying}")

    # Log to CSV
    log_path = "logs/equity_curve.csv"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    file_exists = os.path.isfile(log_path)
    with open(log_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "NetLiq", "BuyingPower"])
        writer.writerow([timestamp, netliq, buying])
    print(f"✅ Logged equity: NetLiq={netliq}, BuyingPower={buying}")

if __name__ == "__main__":
    summary = get_ibkr_equity_summary()
    log_equity_update(summary)