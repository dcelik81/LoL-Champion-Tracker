import requests
from bs4 import BeautifulSoup
import time
import urllib3
from plyer import notification

# SSL sertifika uyarılarını gizle
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- AYARLAR ---
REGION = "tr"
SUMMONER_NAME = "milföysu-1044"
CHAMPION = "morgana"
CHECK_INTERVAL = 3600  # 1 saat (saniye cinsinden)

url = f"https://www.leagueofgraphs.com/tr/summoner/champions/{CHAMPION}/{REGION}/{SUMMONER_NAME}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def get_rank():
    try:
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        if response.status_code != 200:
            print(f"Sayfaya ulaşılamadı. Hata kodu: {response.status_code}")
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Aynı class ismine sahip tüm elementleri buluyoruz
        ranks = soup.find_all("div", class_="number-medium solo-number")
        
        # League of Graphs yapısında genellikle ilk eleman Dünya, ikinci eleman TR sıralamasıdır
        rank_element_world = ranks[0] if len(ranks) > 0 else None
        rank_element_tr = ranks[1] if len(ranks) > 1 else None
        
        results = {}

        if rank_element_world:
            world_text = rank_element_world.text.strip().replace('#', '').replace(',', '')
            results["world"] = int(world_text)
            
        if rank_element_tr:
            tr_text = rank_element_tr.text.strip().replace('#', '').replace(',', '')
            results["tr"] = int(tr_text)

        return results if results else None

    except Exception as e:
        print(f"Hata oluştu: {e}")
        return None

def send_alert(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="LoL Sıralama Takip",
        timeout=10
    )

def track_rank():
    print(f"Takip başlatıldı: {CHAMPION.capitalize()} ({REGION})")
    current_ranks = get_rank()
    
    if current_ranks:
        w_rank = current_ranks.get("world", "N/A")
        t_rank = current_ranks.get("tr", "N/A")
        print(f"Mevcut sıralaman: Dünya #{w_rank}, Türkiye #{t_rank}")
        send_alert("Sıralama Takibi Başladı", f"Dünya: #{w_rank} | Türkiye: #{t_rank}")
    else:
        print("İlk sıralama belirlenemedi, URL'yi kontrol et.")
        current_ranks = {"world": 0, "tr": 0}

    while True:
        time.sleep(CHECK_INTERVAL)
        new_ranks = get_rank()
        
        if new_ranks:
            updates = []
            
            # Türkiye ve Dünya sıralamalarını ayrı ayrı kontrol et
            for key in ["world", "tr"]:
                old = current_ranks.get(key)
                new = new_ranks.get(key)
                label = "Dünya" if key == "world" else "Türkiye"
                
                if old and new:
                    if new > old:
                        msg = f"{label} sıran düştü! (#{old} -> #{new})"
                        updates.append(msg)
                    elif new < old:
                        msg = f"{label} sıran yükseldi! (#{old} -> #{new})"
                        updates.append(msg)
            
            if updates:
                full_msg = "\n".join(updates)
                print(f"GÜNCELLEME:\n{full_msg}")
                send_alert("Sıralama Değişikliği!", full_msg)
                current_ranks = new_ranks
            else:
                print(f"Değişiklik yok. (TR: #{new_ranks.get('tr')}, Dünya: #{new_ranks.get('world')})")

if __name__ == "__main__":
    track_rank()