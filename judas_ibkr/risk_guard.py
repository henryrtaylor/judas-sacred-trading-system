import os
import time
import yaml
from ib_insync import IB

# Path to your risk configuration file
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'risk_config.yml')
CHECK_INTERVAL = 15  # seconds between checks


def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)


def get_account_metrics(ib: IB):
    # Fetch current account metrics from IBKR
    account_values = ib.accountValues()
    metrics = {}
    for av in account_values:
        if av.tag == 'GrossPositionValue':
            metrics['total_position_value'] = float(av.value)
        if av.tag == 'NetLiquidation':
            metrics['net_liq'] = float(av.value)
        if av.tag == 'AvailableFunds':
            metrics['avail_funds'] = float(av.value)
        if av.tag == 'Leverage':
            try:
                metrics['leverage'] = float(av.value)
            except ValueError:
                metrics['leverage'] = 0.0
        if av.tag == 'MarginBalance':
            metrics['margin_balance'] = float(av.value)
    # Compute margin usage ratio
    liq = metrics.get('net_liq', 1)
    margin = metrics.get('margin_balance', 0)
    metrics['margin_usage'] = margin / liq if liq > 0 else 0
    return metrics


def check_risk():
    config = load_config()
    ib = IB()
    port = int(os.getenv('IBKR_API_PORT', 7497))
    ib.connect('127.0.0.1', port, clientId=0)

    metrics = get_account_metrics(ib)
    alerts = []

    # Check max leverage
    max_lev = config.get('max_leverage', 2.0)
    lev = metrics.get('leverage', 0)
    if lev > max_lev:
        alerts.append(f"Leverage {lev:.2f} > max {max_lev}")

    # Check margin usage
    max_margin = config.get('max_margin_usage', 0.8)
    margin_usage = metrics.get('margin_usage', 0)
    if margin_usage > max_margin:
        alerts.append(f"Margin usage {margin_usage:.2f} > max {max_margin}")

    if alerts:
        for a in alerts:
            print(f"⚠️ RISK ALERT: {a}")
    else:
        print(f"✔ Risk OK: leverage={lev:.2f}, margin_usage={margin_usage:.2f}. Next check in {CHECK_INTERVAL}s.")

    ib.disconnect()


if __name__ == '__main__':
    print("🔒 Risk Guard starting…")
    while True:
        check_risk()
        time.sleep(CHECK_INTERVAL)
