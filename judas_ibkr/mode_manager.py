import json
from pathlib import Path

MODE_FILE = Path("judas_mode.json")

DEFAULT_MODE = {
    "mode": "divine",  # Options: divine, standard, hft
    "override_delay": 7,
    "override_enabled": True,
    "require_zion_approval": True
}

def set_mode(mode_name):
    config = DEFAULT_MODE.copy()

    if mode_name == "standard":
        config.update({
            "mode": "standard",
            "override_delay": 2,
            "override_enabled": True,
            "require_zion_approval": False
        })
    elif mode_name == "hft":
        config.update({
            "mode": "hft",
            "override_delay": 0,
            "override_enabled": False,
            "require_zion_approval": False
        })
    elif mode_name == "divine":
        pass  # already loaded as default
    else:
        raise ValueError("Invalid mode. Use 'divine', 'standard', or 'hft'.")

    with open(MODE_FILE, "w") as f:
        json.dump(config, f, indent=2)
    print(f"🔧 Mode set to: {mode_name}")

def get_mode_config():
    if MODE_FILE.exists():
        with open(MODE_FILE, "r") as f:
            return json.load(f)
    else:
        return DEFAULT_MODE

if __name__ == "__main__":
    print("🔍 Current Mode Configuration:")
    print(json.dumps(get_mode_config(), indent=2))