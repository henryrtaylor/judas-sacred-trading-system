from ib_insync import *
from config import IBKR_HOST, IBKR_PORT, CLIENT_ID

# Connect to IBKR
ib = IB()
ib.connect(IBKR_HOST, IBKR_PORT, clientId=CLIENT_ID)

if ib.isConnected():
    print("Connected to IBKR.")

    # Create a contract (e.g., Apple stock)
    contract = Stock('AAPL', 'SMART', 'USD')

    # Request live market data
    ticker = ib.reqMktData(contract, '', False, False)

    # Allow some time for data to populate
    ib.sleep(3)

    # Print market data
    print("\n--- Live Market Data ---")
    print(f"Symbol: {contract.symbol}")
    print(f"Last Price: {ticker.last}")
    print(f"Bid: {ticker.bid}")
    print(f"Ask: {ticker.ask}")
    print(f"Volume: {ticker.volume}")

    # Unsubscribe
    ib.cancelMktData(contract)

else:
    print("Connection failed.")

ib.disconnect()
