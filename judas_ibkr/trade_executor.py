from safe_order import verify_order
from override_check import check_override
from execution_logger import log_execution
from ib_insync import IB, Stock, MarketOrder  # Requires ib_insync installed

def execute_order(symbol, size, side, price, mode="paper", context="manual"):
    try:
        verify_order(symbol, size, side, context)

        if not check_override(seconds=7, flag_path="override/stop.txt"):
            print("⛔ Trade override triggered. Execution skipped.")
            return False

        if mode == "live":
            print(f"🚀 LIVE TRADE: {side} {symbol} size={size} @ {price}")
            ib = IB()
            ib.connect('127.0.0.1', 7497, clientId=1)  # Make sure TWS or Gateway is running

            contract = Stock(symbol.split('-')[0], 'SMART', 'USD')  # Strip suffix like -USD
            order = MarketOrder(side.upper(), abs(size))
            trade = ib.placeOrder(contract, order)
            ib.sleep(1)
            ib.disconnect()
        else:
            print(f"🧪 PAPER TRADE: {side} {symbol} size={size} @ {price}")

        log_execution(symbol, size, side, price, context)
        return True

    except Exception as e:
        print(f"❌ Trade execution failed: {e}")
        return False

# EXAMPLE USAGE
if __name__ == "__main__":
    execute_order(symbol="AAPL", size=10, side="BUY", price=185.50, mode="paper", context="Test Rebalance")