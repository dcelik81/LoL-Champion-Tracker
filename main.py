import requests
from bs4 import BeautifulSoup
import time

# Bilgilerini buraya gir
REGION = "tr"
SUMMONER_NAME = "milföysu#1044" # Riot ID ve Tag formatında
CHAMPION = "morgana"

# League of Graphs URL (Örnektir, profil sayfana göre düzenlenmeli)
url = f"https://www.leagueofgraphs.com/tr/summoner/champions/{CHAMPION}/{REGION}/{SUMMONER_NAME.replace('#', '-')}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_rank():
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Sıralama bilgisinin olduğu HTML elementini bul (Bu kısım site yapısına göre güncellenmelidir)
        rank_element = soup.select_one('.rank-number') 
        if rank_element:
            return int(rank_element.text.strip().replace('#', ''))
        return None
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return None

def track_rank():
    current_rank = get_rank()
    print(f"Takip başlatıldı. Mevcut sıralaman: {current_rank}")
    
    while True:
        time.sleep(3600) # Her 1 saatte bir kontrol et
        new_rank = get_rank()
        
        if new_rank and new_rank > current_rank:
            print(f"UYARI: Sıralaman düştü! Yeni sıran: {new_rank}")
            # Buraya Windows bildirimi veya sesli uyarı eklenebilir
            current_rank = new_rank
        elif new_rank and new_rank < current_rank:
            print(f"TEBRİKLER: Sıralaman yükseldi! Yeni sıran: {new_rank}")
            current_rank = new_rank

if __name__ == "__main__":
    track_rank()

