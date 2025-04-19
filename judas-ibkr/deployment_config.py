# 🔱 JUDAS DEPLOYMENT CONFIGURATION
# This file governs deployment mode, safety, and sacred filters.

# Deployment Mode
LIVE_MODE = False  # ← Set to True when you are ready to trade real funds

# Trade Safety Settings
REQUIRE_AGENT_CONSENSUS = True    # All agents must align for live trade
CONFIRM_BEFORE_EXECUTE = True     # Ask for manual confirmation in LIVE mode
RESTRICT_TO_MARKET_HOURS = True   # Do not allow trades outside 9AM–4PM

# Sacred Behavior
SANCTUARY_SYMBOLS = ["ARKK", "XLY", "TSLA"]  # These receive extra reverence
DIVINE_PAUSE_ON_FOMC = True  # Prevent trades on holy market days (see holy_days.py)

# Logging / Awareness
LOG_ALL_TRADES = True
ENABLE_REFLECTIVE_MODE = True  # Enables judas_reflector to activate post-trade
