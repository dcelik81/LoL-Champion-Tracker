import json
import os

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".LoLChampionTracker", "config.json")

DEFAULT_CONFIG = {
    "REGION": "KR",
    "SUMMONER_NAME": "Hide+on+bush-KR1",
    "CHAMPION": "ryze",
    "CHECK_INTERVAL": 600,
    "LANGUAGE": "en"
}

def load_config():
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_CONFIG, f, indent=4, ensure_ascii=False)
        return DEFAULT_CONFIG
    
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

config = load_config()
