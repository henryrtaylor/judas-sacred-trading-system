import logging

def execute_trade(signal, symbol, qty=10, paper=True):
    logging.info(f"Signal: {signal} | Symbol: {symbol} | Qty: {qty} | Paper Mode: {paper}")
    # Placeholders for real trading execution
    if signal == 'BUY':
        print(f"Buying {qty} shares of {symbol}")
    elif signal == 'SELL':
        print(f"Selling {qty} shares of {symbol}")
    else:
        print("No action taken")
