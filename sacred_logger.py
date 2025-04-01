# sacred_logger.py
import datetime
from pathlib import Path

def log_event(source: str, message: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_path = Path("logs")
    log_path.mkdir(exist_ok=True)

    log_file = log_path / "judas_diagnostics.log"
    entry = f"[{timestamp}] [{source.upper()}] {message}\n"

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)

    # Optional real-time echo to terminal
    print(entry.strip())
