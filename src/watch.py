import requests
import subprocess
import time

from urllib.parse import urlparse, parse_qs

class watch_anime:
    def __init__(self, use_vlc=False):
        self.base_url = "https://www.mangacix.net/"
        self.use_vlc = use_vlc
    def open_with_video_player(self,url):
        try:
            if not isinstance(url, str):
                raise ValueError("Url string olmalı.")
            
            if self.use_vlc:
                subprocess.run(['vlc','--fullscreen','-v', url], check=True, capture_output=True, text=True)
            else:
                subprocess.run(['mpv','--fullscreen', url], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Oynatılırken Hata Oluştu: {e}")
        except ValueError as e:
            print(f"Bir Hata Oluştu: {e}")


    def fetch_anime_api_watch_url(self,url):
        wtch_url = f"https://animecix.net/{url}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(wtch_url, headers=headers, allow_redirects=True)
        response.raise_for_status()

        # Gerekli, Gereksiz? Tartışılır.
        time.sleep(3)

        final_resp = response.url

        path = urlparse(final_resp).path
        embed_id = path.split('/')[2]  # Örneğin: '63116f91a21596c7104eac99'
        query = urlparse(final_resp).query
        params = parse_qs(query)
        vid = params.get('vid', [None])[0]  # Örneğin: '363320'

        watch_url = f"https://tau-video.xyz/api/video/{embed_id}?vid={vid}"

        response = requests.get(watch_url)
        response.raise_for_status()
        data = response.json()
        urls = []
        for item in data.get('urls', []):
            episode_url = item.get('url', 'No URL field')
            urls.append({'url': episode_url})
        return urls

    def anime_watch(self, url_list):
        if not isinstance(url_list, list) or not url_list:
            print("Geçerli bir url bulunamadı! ")
            return
        url_indices_to_try = [3,2, 1, 0]

        for index in url_indices_to_try:
            if index < len(url_list):
                url = url_list[index]['url']
                try:
                    self.open_with_video_player(url)
                    print(f"Bölüm Oynatılıyor... {index}.")
                    return
                except Exception as e:
                    print(f"Bölüm oynatılırken hata oluştu! {index}: {e}")
        self.open_with_video_player(url)
