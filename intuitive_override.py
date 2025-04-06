import json
from datetime import datetime

override_log = []

def apply_override(signal, override_params):
    signal.update(override_params)
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "override": override_params,
        "original_signal": signal
    }
    override_log.append(log_entry)
    return signal

def export_log():
    with open("override_log.json", "w") as f:
        json.dump(override_log, f, indent=2)