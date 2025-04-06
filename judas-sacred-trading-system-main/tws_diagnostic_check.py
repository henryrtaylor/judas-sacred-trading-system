import socket
import subprocess
import platform
import json

HOST = '127.0.0.1'
PORTS = [7497, 7496, 4001, 4002]  # Common TWS/IBG ports
TIMEOUT = 2
CONFIG_FILE = "tws_auto_config.json"

def is_port_open(host, port, timeout):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (ConnectionRefusedError, socket.timeout, OSError):
        return False

def allow_firewall_port(port):
    if platform.system() == 'Windows':
        try:
            rule_name = f"Allow_TWS_Port_{port}"
            subprocess.run([
                "netsh", "advfirewall", "firewall", "add", "rule",
                f"name={rule_name}", f"dir=in", f"action=allow",
                f"protocol=TCP", f"localport={port}"
            ], check=True, stdout=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            pass

# Auto-detect open port
open_ports = []
selected_port = None
for port in PORTS:
    allow_firewall_port(port)
    if is_port_open(HOST, port, TIMEOUT):
        open_ports.append(port)
        if selected_port is None:
            selected_port = port

# Export the result
if selected_port:
    config = {
        "host": HOST,
        "port": selected_port,
        "clientId": 1
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    print(f"✅ Selected and saved open port: {selected_port} in {CONFIG_FILE}")
else:
    print("❌ No open ports found. Cannot connect to TWS or IB Gateway.")

# REUSABLE CONFIG LOADER FOR ALL SCRIPTS

def load_ibkr_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {"host": HOST, "port": 7497, "clientId": 1}  # fallback
