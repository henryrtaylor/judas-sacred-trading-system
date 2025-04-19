from ib_insync import *
import pandas as pd

def fetch_market_data(symbol: str, duration='1 D', barSize='5 mins'):
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)
    contract = Stock(symbol, 'SMART', 'USD')
    bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr=duration,
        barSizeSetting=barSize,
        whatToShow='TRADES',
        useRTH=True,
        formatDate=1
    )
    df = util.df(bars)
    ib.disconnect()
    return df
