import os, json
from pathlib import Path

# v62.0 Persistence Standard
# Stores config in user home to avoid permission issues
CONFIG_DIR = Path.home() / "Nighthawk_Suite"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_FILE = CONFIG_DIR / "nighthawk_config.json"

def load_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except: pass
    return {"handle": "UNKNOWN OPERATOR", "god_mode_threshold": -75}

def save_config(handle):
    data = {"handle": handle, "god_mode_threshold": -75}
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(data, f)
    except Exception as e:
        print(f"[!] Config Save Error: {e}")
    return data
