import os
from ib_insync import *
from config import IBKR_HOST, IBKR_PORT, CLIENT_ID
from utils.summary import print_account_summary

# Optional: Set encoding environment variable
os.environ["PYTHONUTF8"] = "1"

# Connect to IBKR
ib = IB()
ib.connect(IBKR_HOST, IBKR_PORT, clientId=CLIENT_ID)

# Confirm connection
if ib.isConnected():
    print("Connected to IBKR.")

    # Request account summary
    summary = ib.reqAccountSummary()
    ib.sleep(2)  # Let the API respond

    # Debug: Print raw summary result
    print("\nRaw summary result:")
    print(summary)

    # Print nicely formatted output
    if summary:
        print_account_summary(summary)
    else:
        print("⚠️ No account summary returned. Check API settings in TWS or IB Gateway.")
else:
    print("❌ Connection to IBKR failed.")

ib.disconnect()
