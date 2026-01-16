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

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

toaster = ToastNotifier()

REGION = "tr"
SUMMONER_NAME = "milföysu-1044"
CHAMPION = "morgana"
CHECK_INTERVAL = 300 

url = f"https://www.leagueofgraphs.com/tr/summoner/champions/{CHAMPION}/{REGION}/{SUMMONER_NAME}"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36..."}

current_ranks = {"world": 0, "tr": 0}

def get_rank():
    logger.info(f"Sıralama kontrol ediliyor: {SUMMONER_NAME}")
    try:
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        ranks = soup.find_all("div", class_="number-medium solo-number")
        
        results = {}
        if len(ranks) >= 2:
            results["world"] = int(ranks[0].text.strip().replace('#', '').replace(',', ''))
            results["tr"] = int(ranks[1].text.strip().replace('#', '').replace(',', ''))
            logger.info("Veri başarıyla çekildi.")
            logger.info(f"Veriler: {results}")
            return results
        
        logger.warning("Sıralama verisi site içinde bulunamadı.")
        return None
    except Exception as e:
        logger.error(f"Hata oluştu: {e}")
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
        msg = f"Dünya: #{new_ranks['world']} | TR: #{new_ranks['tr']}"
        send_alert("Güncel Sıralaman", msg)
        current_ranks = new_ranks
    else:
        send_alert("Hata", "Veri çekilemedi. Detayları log dosyasında bulabilirsiniz.")

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

icon = Icon("LoL Sıralama", load_icon(), menu=Menu(
    MenuItem("Güncel Sıralamayı Çek", manual_check),
    MenuItem("Kapat", on_quit)
))

if __name__ == "__main__":
    threading.Thread(target=background_task, daemon=True).start()
    manual_check()
    icon.run()
