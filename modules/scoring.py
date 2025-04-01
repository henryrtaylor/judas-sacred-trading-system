# modules/scoring.py

import numpy as np

def score_strategy_stock(df):
    """
    Score stock based on simple momentum and SMA crossover.
    """
    df = df.copy()
    df['sma_5'] = df['close'].rolling(window=5).mean()
    df['sma_20'] = df['close'].rolling(window=20).mean()
    df['momentum'] = df['close'].pct_change(periods=3)
    
    if df[['sma_5', 'sma_20', 'momentum']].isnull().any().any():
        return None

    recent = df.iloc[-1]
    score = 0
    if recent['sma_5'] > recent['sma_20']:
        score += 0.6
    score += max(0, min(0.4, recent['momentum']))
    return round(score, 4)

def score_strategy_forex(df):
    """
    Simple scoring for forex based on volatility and recent trend.
    """
    df = df.copy()
    df['volatility'] = df['close'].pct_change().rolling(window=5).std()
    df['trend'] = df['close'].pct_change(periods=3)

    if df[['volatility', 'trend']].isnull().any().any():
        return None

    recent = df.iloc[-1]
    score = max(0, min(1.0, (recent['trend'] + recent['volatility']) / 0.05))
    return round(score, 4)

def score_strategy_crypto(df):
    """
    Score crypto based on breakout detection.
    """
    df = df.copy()
    df['high_20'] = df['high'].rolling(window=20).max()
    df['breakout'] = df['close']
