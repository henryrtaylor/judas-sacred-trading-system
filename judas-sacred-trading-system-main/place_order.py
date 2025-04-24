from ib_insync import *
from config import IBKR_HOST, IBKR_PORT, CLIENT_ID
from utils.logger import log_trade  # 📄 Import logger for trade logging

ib = IB()
ib.connect(IBKR_HOST, IBKR_PORT, clientId=CLIENT_ID)

if ib.isConnected():
    print("✅ Connected to IBKR")

    # Define contract (e.g., buy 10 shares of AAPL)
    contract = Stock('AAPL', 'SMART', 'USD')

    # Define the order (Market or Limit)
    order = MarketOrder('BUY', 10)  # Change to LimitOrder if you want a price

    # Place the order
    trade = ib.placeOrder(contract, order)
    print(f"\n🚀 Placing order: {order.action} {order.totalQuantity} {contract.symbol}")

    # Wait until it fills or updates
    ib.sleep(2)
    ib.waitOnUpdate(timeout=5)

    # Order status
    print(f"\n📦 Order Status: {trade.orderStatus.status}")
    print(f"Filled: {trade.orderStatus.filled} @ Avg Price: {trade.orderStatus.avgFillPrice}")

    # Log the trade to CSV
    log_trade(contract, order, trade.orderStatus)

else:
    print("❌ Connection failed.")

ib.disconnect()
