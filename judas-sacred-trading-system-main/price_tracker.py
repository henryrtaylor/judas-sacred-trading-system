from ib_insync import *
from config import IBKR_HOST, IBKR_PORT, CLIENT_ID

# Set up and connect
ib = IB()
ib.connect(IBKR_HOST, IBKR_PORT, clientId=CLIENT_ID)

if ib.isConnected():
    print("✅ Connected to IBKR")

    # Choose instrument (you can change this)
    contract = Forex('EURUSD')
    ticker = ib.reqMktData(contract)

    print("📈 Tracking EURUSD...\n(Press CTRL+C to stop)\n")

    try:
        while True:
            ib.sleep(1)  # Wait 1 second between updates
            print(f"Bid: {ticker.bid} | Ask: {ticker.ask} | Last: {ticker.last}")
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user.")

    ib.cancelMktData(contract)
    ib.disconnect()

else:
    print("❌ Connection failed.")
