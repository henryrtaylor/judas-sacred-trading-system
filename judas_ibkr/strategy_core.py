def simple_strategy(df):
    latest = df.iloc[-1]
    if latest['rsi'] < 30 and latest['close'] > latest['sma_long']:
        return 'BUY'
    elif latest['rsi'] > 70:
        return 'SELL'
    else:
        return 'HOLD'
