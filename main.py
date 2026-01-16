import requests
from bs4 import BeautifulSoup
import time
import urllib3
import threading
import sys
from win10toast import ToastNotifier
from pystray import Icon, Menu, MenuItem
from PIL import Image
from logger import logger
import os
from config_manager import config
from translations import get_translations, get_champion

current_lang_code = config.get("LANGUAGE", "tr")
T = get_translations(current_lang_code)

REGION = config.get("REGION", "KR")
SUMMONER_NAME = config.get("SUMMONER_NAME", "Hide+on+bush-KR1")
CHAMPION = get_champion(config.get("CHAMPION", "ryze"))
CHECK_INTERVAL = config.get("CHECK_INTERVAL", 600)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

toaster = ToastNotifier()

url = f"https://www.leagueofgraphs.com/tr/summoner/champions/{config.get("CHAMPION", "ryze")}/{REGION}/{SUMMONER_NAME}"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36..."}

current_ranks = {"world": 0, REGION: 0}

def get_rank():
    logger.info(f"{T['searching']}: {url}")
    logger.info(f"{T['searching']}: {SUMMONER_NAME} - {CHAMPION} - {REGION}")
    try:
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        ranks = soup.find_all("div", class_="number-medium solo-number")
        
        results = {}
        if len(ranks) >= 2:
            results["world"] = int(ranks[0].text.strip().replace('#', '').replace(',', ''))
            results[REGION] = int(ranks[1].text.strip().replace('#', '').replace(',', ''))
            logger.info(T['fetching_success'])
            logger.info(f"{T['datas']}: {results}")
            return results
        
        logger.warning(T['data_not_found'])
        return None
    except Exception as e:
        logger.error(f"{T['error_title']}: {e}")
        return None

def send_alert(title, message):
    ico_path = resource_path("icon.ico")
    
    if not os.path.exists(ico_path):
        ico_path = None
        
    toaster.show_toast(
        title, 
        message, 
        icon_path=ico_path,
        duration=5, 
        threaded=True
    )

def manual_check():
    global current_ranks
    new_ranks = get_rank()
    if new_ranks:
        msg = f"{SUMMONER_NAME.split('-')[0]}\n{T['world']}: #{new_ranks['world']} | {T[REGION]}: #{new_ranks[REGION]}"
        send_alert(f"{T['alert_title']} {CHAMPION}", msg)
        current_ranks = new_ranks
    else:
        send_alert(T['error_title'], T['error_msg'])

def background_task():
    global current_ranks
    while True:
        time.sleep(CHECK_INTERVAL)
        new_ranks = get_rank()
        if new_ranks and new_ranks != current_ranks:
            current_ranks = new_ranks

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def load_icon():
    path = resource_path("icon.ico")
    img = Image.open(path)
    return img

def on_quit(icon, item):
    icon.stop()
    sys.exit()

icon = Icon(
    f"LoL {T['alert_title']} {CHAMPION}", 
    load_icon(),
    menu=Menu(
        MenuItem(f"{T['menu_check']}", manual_check),
        MenuItem(f"{T['menu_quit']}", on_quit)
    )
)

if __name__ == "__main__":
    threading.Thread(target=background_task, daemon=True).start()
    manual_check()
    icon.run()
