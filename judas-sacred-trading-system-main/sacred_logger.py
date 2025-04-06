# sacred_logger.py
from datetime import datetime
from pathlib import Path

def log_event(scope: str, message: str, file: str = "logs/judas_diagnostics.log"):
    Path("logs").mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{timestamp} [{scope.upper()}] {message}\n"

    with open(file, "a", encoding="utf-8") as f:
        f.write(line)
    print(line.strip())
