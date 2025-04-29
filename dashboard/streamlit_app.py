import streamlit as st
import pandas as pd
import os

from utils.risk_insights_manager import RiskInsightsManager
from utils.spirit_coin_adapter import SpiritPriceAdapter

# ——— Streamlit Page Config ———
st.set_page_config(
    page_title="Judas Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ——— Sidebar: Alerts & Settings ———
st.sidebar.header("🔧 Settings")
drawdown_alert = st.sidebar.slider(
    "Max Drawdown Alert (%)",
    min_value=0.5,
    max_value=10.0,
    value=5.0,
    step=0.5
)
volatility_alert = st.sidebar.slider(
    "Volatility Alert Threshold",
    min_value=0.0,
    max_value=0.1,
    value=0.02,
    step=0.005
)
rolling_window = st.sidebar.number_input(
    "Rolling Window (points)",
    min_value=5,
    max_value=100,
    value=20,
    step=5
)

# ——— Instantiate Risk Insights ———
risk_insights = RiskInsightsManager(
    alert_thresholds={'drawdown': drawdown_alert, 'volatility': volatility_alert},
    rolling_window=rolling_window
)

# ——— Load Data ———
# Ensure your Rebalancer writes these CSVs during execution
DATA_DIR = os.path.join(os.getcwd(), "dashboard", "data")

equity_path = os.path.join(DATA_DIR, "equity.csv")
trades_path = os.path.join(DATA_DIR, "trades.csv")

if os.path.exists(equity_path):
    eq_df = pd.read_csv(equity_path, parse_dates=["timestamp"]).set_index("timestamp")
    st.subheader("📈 Equity Curve")
    st.line_chart(eq_df["equity"])
    # Record into insights
    for val in eq_df["equity"]:
        risk_insights.record_equity(val)
else:
    st.warning(f"Equity file not found at {equity_path}")

if os.path.exists(trades_path):
    trades_df = pd.read_csv(trades_path, parse_dates=["timestamp"])
    st.subheader("📄 Trade Log")
    st.dataframe(trades_df)
    # Optionally record P&L
    if "pnl" in trades_df.columns:
        for pnl in trades_df["pnl"]:
            risk_insights.record_trade(pnl)
else:
    st.warning(f"Trades file not found at {trades_path}")

# ——— SPIRIT Price Widget ———
st.subheader("🪩 SPIRIT Token")
price_adapter = SpiritPriceAdapter()
spirit_price = price_adapter.get_price()
st.metric(label="SPIRIT Price (USD)", value=f"${spirit_price:.4f}")

# ——— Risk Summary & Alerts ———
st.subheader("⚠️ Risk Insights Summary")
summary = risk_insights.summary()
st.json(summary)

# Trigger alert checks
risk_insights.check_alerts()
