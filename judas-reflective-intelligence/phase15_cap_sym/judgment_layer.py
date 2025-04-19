from log_to_sheet import log_to_sheet

def evaluate_signal(symbol, tf_agree: bool, confidence: float):
    if not tf_agree:
        log_to_sheet("judgment_logs", action="SKIPPED", symbol=symbol, outcome="TIMEFRAME_MISMATCH", notes=f"conf={confidence}")
        return False
    if confidence < 0.5:
        log_to_sheet("judgment_logs", action="SKIPPED", symbol=symbol, outcome="LOW_CONFIDENCE", notes=f"conf={confidence}")
        return False
    log_to_sheet("judgment_logs", action="PASS", symbol=symbol, outcome="VALIDATED", notes=f"conf={confidence}")
    return True