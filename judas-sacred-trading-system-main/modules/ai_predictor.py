# modules/ai_predictor.py
# ✨ Judas AI Prediction Module (Enhanced for Stability & Clean Fallbacks)

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
from sacred_logger import log_event

# Main prediction function
def predict_stock_signal(df: pd.DataFrame) -> float:
    df = df.copy()
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df = df.dropna(subset=["close"])

    if len(df) < 20:
        log_event("ai", f"❌ Not enough data rows to compute prediction ({len(df)} rows)")
        return None

    # Features
    df["ma_3"] = df["close"].rolling(window=3).mean()
    df["ma_7"] = df["close"].rolling(window=7).mean()
    df["momentum"] = df["close"].pct_change(periods=3)
    df["volatility"] = df["close"].rolling(window=5).std()
    df["target"] = (df["close"].shift(-1) > df["close"]).astype(int)  # Will it go up tomorrow?

    df = df.dropna()
    features = ["ma_3", "ma_7", "momentum", "volatility"]
    X = df[features]
    y = df["target"]

    if len(X) == 0 or len(y) == 0:
        log_event("ai", f"❌ No valid feature rows to train AI on")
        return None

    # Normalize & train simple model
    scaler = StandardScaler()
    try:
        X_scaled = scaler.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)
        model = LogisticRegression()
        model.fit(X_train, y_train)

        # Predict on latest row
        latest = scaler.transform([X.iloc[-1]])
        prob = model.predict_proba(latest)[0][1]  # Probability it goes up

        return round(prob, 4)

    except Exception as e:
        log_event("ai", f"❌ AI training/prediction error: {str(e)}")
        return None
