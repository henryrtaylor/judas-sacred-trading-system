from ib_insync import *
from config import IBKR_HOST, IBKR_PORT, CLIENT_ID
import pandas as pd

ib = IB()
ib.connect(IBKR_HOST, IBKR_PORT, clientId=CLIENT_ID)

if ib.isConnected():
    print("✅ Connected to IBKR\n")

    account_summary = ib.accountSummary()
    positions = ib.positions()

    net_liq = float([x.value for x in account_summary if x.tag == 'NetLiquidation'][0])
    print(f"💼 Net Liquidation (Estimate): ${net_liq:,.2f}")

    rows = []
    for pos in positions:
        contract = pos.contract
        estimated_value = pos.avgCost * pos.position
        rows.append({
            'symbol': contract.symbol,
            'type': contract.secType,
            'qty': pos.position,
            'avgCost': pos.avgCost,
            'est_value': estimated_value,
            'pct_of_portfolio': (estimated_value / net_liq) * 100
        })

    df = pd.DataFrame(rows)
    df = df.sort_values(by='pct_of_portfolio', ascending=False)

    print("\n📊 Portfolio Snapshot (Fallback Mode):\n")
    print(df.to_string(index=False, float_format=lambda x: f"${x:,.2f}" if isinstance(x, float) else f"{x}"))

else:
    print("❌ IBKR connection failed.")

ib.disconnect()
