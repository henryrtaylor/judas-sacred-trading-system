# connection.py
# Handles connection to IBKR API via ib_insync

from ib_insync import IB

def connect_to_ibkr(host='127.0.0.1', port=7497, client_id=1):
    ib = IB()
    ib.connect(host, port, clientId=client_id)
    return ib
