import requests
from bs4 import BeautifulSoup
import time
import urllib3
import threading
import sys
from win10toast import ToastNotifier
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

# SSL uyarılarını kapat
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
toaster = ToastNotifier()

# --- AYARLAR ---
REGION = "tr"
SUMMONER_NAME = "milföysu-1044"
CHAMPION = "morgana"
CHECK_INTERVAL = 300 

url = f"https://www.leagueofgraphs.com/tr/summoner/champions/{CHAMPION}/{REGION}/{SUMMONER_NAME}"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36..."}

current_ranks = {"world": 0, "tr": 0}

def get_rank():
    try:
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        ranks = soup.find_all("div", class_="number-medium solo-number")
        
        results = {}
        if len(ranks) >= 2:
            results["world"] = int(ranks[0].text.strip().replace('#', '').replace(',', ''))
            results["tr"] = int(ranks[1].text.strip().replace('#', '').replace(',', ''))
            return results
        return None
    except:
        return None

def send_alert(title, message):
    toaster.show_toast(title, message, duration=5, threaded=True)

def manual_check(icon=None):
    """Menüden tıklandığında anlık kontrol yapar."""
    global current_ranks
    new_ranks = get_rank()
    if new_ranks:
        msg = f"Dünya: #{new_ranks['world']} | TR: #{new_ranks['tr']}"
        send_alert("Güncel Sıralaman", msg)
        current_ranks = new_ranks
    else:
        send_alert("Hata", "Veri çekilemedi.")

def background_task():
    """Arka planda periyodik kontrol yapar."""
    global current_ranks
    while True:
        time.sleep(CHECK_INTERVAL)
        new_ranks = get_rank()
        if new_ranks and new_ranks != current_ranks:
            # Karşılaştırma ve bildirim mantığı buraya...
            current_ranks = new_ranks

def load_icon():
    img = Image.open("icon.JPG")
    return img

def on_quit(icon, item):
    icon.stop()
    sys.exit()

# System Tray Menüsü
icon = Icon("LoL Sıralama", load_icon(), menu=Menu(
    MenuItem("Güncel Sıralamayı Çek", manual_check),
    MenuItem("Kapat", on_quit)
))

if __name__ == "__main__":
    # Arka plan kontrolünü ayrı bir thread olarak başlat
    threading.Thread(target=background_task, daemon=True).start()
    
    # Program başlar başlamaz bir kontrol yap
    manual_check()
    
    # Tray ikonunu çalıştır
    icon.run()
