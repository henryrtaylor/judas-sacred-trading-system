from ib_insync import *
from config import IBKR_HOST, IBKR_PORT, CLIENT_ID

ib = IB()
ib.connect(IBKR_HOST, IBKR_PORT, clientId=CLIENT_ID)

if ib.isConnected():
    print("✅ Connected to IBKR\n")

    # Get open positions
    positions = ib.positions()

    if positions:
        print("--- Current Portfolio ---\n")
        for pos in positions:
            contract = pos.contract
            print(f"{contract.symbol:<10} {contract.secType:<6} {pos.position:>8} @ Avg Price: {pos.avgCost:.2f}")
    else:
        print("📭 No open positions.")

    # Get account values like Net Liquidation, Cash, etc.
    account = ib.accountValues()
    print("\n--- Account Values ---\n")
    for item in account:
        if item.tag in ['NetLiquidation', 'TotalCashValue', 'RealizedPnL', 'UnrealizedPnL']:
            print(f"{item.tag:<20} {item.value:>10} {item.currency}")

else:
    print("❌ Connection failed.")

ib.disconnect()
