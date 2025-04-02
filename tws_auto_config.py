# tws_auto_config.py
# 🔌 Auto-detect best open TWS/IBKR port

import socket

CANDIDATE_PORTS = [7497, 7496, 4001, 4002]
DEFAULT_HOST = "127.0.0.1"
CLIENT_ID = 1


def is_port_open(port):
    try:
        with socket.create_connection((DEFAULT_HOST, port), timeout=2):
            return True
    except Exception:
        return False


def get_ibkr_settings():
    for port in CANDIDATE_PORTS:
        if is_port_open(port):
            print(f"✅ Using IBKR port: {port}")
            return DEFAULT_HOST, port, CLIENT_ID

    print("❌ No open IBKR ports found. Defaulting to 7497.")
    return DEFAULT_HOST, 7497, CLIENT_ID


if __name__ == "__main__":
    print(get_ibkr_settings())
