import json
import os

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".LoLChampionTracker", "config.json")

DEFAULT_CONFIG = {
    "REGION": "tr",
    "SUMMONER_NAME": "milföysu-1044",
    "CHAMPION": "morgana",
    "CHECK_INTERVAL": 300,
    "LANGUAGE": "tr"
}

def load_config():
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_CONFIG, f, indent=4, ensure_ascii=False)
        return DEFAULT_CONFIG
    
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

config = load_config()
