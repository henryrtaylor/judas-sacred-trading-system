import asyncio
import os
from datetime import datetime
from ib_insync import IB
import argparse

async def log_equity(interval_seconds: int = 60):
    ib = IB()
    ib_host = os.getenv('IBKR_HOST', '127.0.0.1')
    ib_port = int(os.getenv('IBKR_API_PORT', '7497'))
    client_id = 2

    await ib.connectAsync(ib_host, ib_port, clientId=client_id)
    print(f"[EquityLogger] Connected to IBKR at {ib_host}:{ib_port}")

    while True:
        account_summary = await ib.accountSummaryAsync()
        if account_summary:
            net_liq = float(account_summary.get('NetLiquidation', 0))
            cash_balance = float(account_summary.get('AvailableFunds', 0))
            buying_power = float(account_summary.get('BuyingPower', 0))

            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] NetLiq: ${net_liq:.2f}, Cash: ${cash_balance:.2f}, Buying Power: ${buying_power:.2f}")
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Warning: No account summary received.")

        await asyncio.sleep(interval_seconds)

async def main():
    parser = argparse.ArgumentParser(description="Equity Logger for IBKR Account")
    parser.add_argument('--loop', type=int, default=60, help='Interval for logging equity data in seconds')
    args = parser.parse_args()

    await log_equity(args.loop)

if __name__ == "__main__":
    asyncio.run(main())
