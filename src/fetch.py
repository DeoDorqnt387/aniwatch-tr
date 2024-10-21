import requests
import time

from urllib.parse import urlparse, parse_qs

class FetchData_a:
    def __init__(self):
        self.base_url = "https://animecix.net/"
        self.video_players = ["tau-video.xyz", "sibnet"]
        self.headers = {'Accept': 'application/json','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    def _get_json(self, url):
        """Jon Verisini Al"""
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def fetch_anime_srch_dt(self, query):
        """Arama Verisi"""
        #https://animecix.net/secure/search/date%20a%20l?type=&limit=8
        search_url = f"{self.base_url}/secure/search/{query}?type=&limit=20"
        data = self._get_json(search_url)
        return [{'name': item.get('name'), 'id': item.get('id'), 'type': item.get('type')} for item in data.get('results', [])]

    def fetch_anime_srch_seasons(self, selected_id):
        """Sezonsal Veri"""
        url = f"{self.base_url}secure/related-videos?episode=1&season=1&titleId={selected_id}"
        json_data = self._get_json(url)

        videos = json_data.get("videos", [])

        print(f"Sezon Sayısı Belirleniyor...")
        time.sleep(0.5)
        print(f"malID Çıkarılıyor...")
        time.sleep(0.5)
        print(f"Veri Tipi Alınıyor...")

        if videos and isinstance(videos, list) and len(videos) > 0:
            seasons = videos[0].get('title', {}).get('seasons', [])
            if seasons:
                if isinstance(seasons, list):
                    return list(range(len(seasons)))
            else:
                print("Err!")
                return []

    def fetch_anime_srch_eps(self, selected_id):
        """Bölüm Verisi"""
        seasons = self.fetch_anime_srch_seasons(selected_id)
        if seasons:
            episodes = []
            seen_episode_names = set()

            for season_index in seasons:
                srch_eps_data_url = f"{self.base_url}secure/related-videos?episode=1&season={season_index + 1}&titleId={selected_id}"
                data = self._get_json(srch_eps_data_url)
                for item in data.get('videos', []):
                    episode_name = item.get('name', "No url field")
                    if episode_name not in seen_episode_names:
                        episode_url = item.get('url', 'No name field')
                        episode_thumbnail = item.get('thumbnail', "No thumbnail field")
                        episodes.append({'name': episode_name, 'url': episode_url, 'thumbnail': episode_thumbnail})
                        seen_episode_names.add(episode_name)
            return episodes
        else:
            print("hata")

    def fetch_anime_watch_api_url(self, url):
        """İzleme Urlsini al"""
        wtch_url = f"{self.base_url}{url}"                                          
        try:
            response = requests.get(wtch_url, headers=self.headers, allow_redirects=True)
            response.raise_for_status()

            time.sleep(3)

            final_resp = response.url

            path = urlparse(final_resp).path
            embed_id = path.split('/')[2]
            query = urlparse(final_resp).query
            params = parse_qs(query)
            vid = params.get('vid', [None])[0]

            watch_url = f"https://{self.video_players[0]}/api/video/{embed_id}?vid={vid}"
            wtch_resp = requests.get(watch_url)
            wtch_resp.raise_for_status()
            data = wtch_resp.json()
            urls = []
            for item in data.get('urls', []):
                episode_url = item.get('url', 'No URL field')
                urls.append({'url': episode_url})
            return urls            
        except Exception as e:
            print("Hata Oluştu!", e)
            return []

    def fetch_anime_watch_api_url_movie(self,selected_id):
        """İzleme Urlsini Al (Movie)"""
        """YAZACAĞIM KODU SEVİM AMK BU NE"""
        url = f"https://animecix.net/secure/titles/{selected_id}"
        json_dt = self._get_json(url)
        url_vid = json_dt.get("title", {}).get("videos", [{}])[0].get("url")
        if url_vid:
            try:
                path = urlparse(url_vid).path
                embed_id = path.split("/")[2]
                api_url = f"https://{self.video_players[0]}/api/video/{embed_id}"
                video_data = self._get_json(api_url)
                
                try_best_qua = ["1080p", "720p", "480p"]
                
                selected_url = None
                for quality in try_best_qua:
                    for url_info in video_data.get('urls', []):
                        if url_info.get("label") == quality:
                            selected_url = url_info.get("url")
                            break
                    if selected_url:
                        break
            
                return selected_url
            except:
                if self.video_players[1] in url_vid:
                    selected_url = url_vid+".mp4"
                    
                return selected_url
        return None

class FetchData_b:
    def __init__(self):
        self.player="https://tp1---av-u0g3jyaa-8gcu.oceanicecdn.xyz"
        self.base_url = "https://api.openani.me"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}


    def fetch_anime_srch_data(self, yr_rsp):
        """Arama Verisi"""
        search_url = f"{self.base_url}/anime/search?q={yr_rsp}"
        resp = requests.get(search_url, headers=self.headers)
        resp.raise_for_status()
        
        data = resp.json()
        return [{'name': anime.get('english'), 'slug': anime.get('slug')} for anime in data]

    def fetch_anime_seasons_data(self, slug):
        """Anime Sezon Verisini Al"""
        url = f"{self.base_url}/anime/{slug}"
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        
        data = resp.json()
        seasons_count = data["numberOfSeasons"]
        malID = data["malID"]
        type = data["type"]

        print(f"Sezon Sayısı Belirleniyor...")
        time.sleep(0.5)
        print(f"malID Çıkarılıyor...")
        time.sleep(0.5)
        print(f"Veri Tipi Alınıyor...")

        return seasons_count, slug, malID

    def fetch_anime_seasons_episodes(self, slug):
        """Anime Sezon, Bölüm, Ad Verisini Al"""
        season_count, slug, malID = self.fetch_anime_seasons_data(slug)
        if not season_count:
            print("Sezon bulunamadı.")
            return []

        all_episodes = []
        season_numbers = []

        for season in range(1, season_count + 1):
            url = f"{self.base_url}/anime/{slug}/season/{season}"
            resp = requests.get(url, headers=self.headers)
            resp.raise_for_status()

            data = resp.json()
            episodes = data["season"]["episodes"]
            season_number = data["season"]["season_number"]

            print(f"Total Episodes in Season {season}: {len(episodes)}")

            all_episodes.extend(episodes)
            season_numbers.extend([season_number] * len(episodes))

        episode_list = [
            (episode.get("name"), episode.get("episodeNumber"), season_number)
            for episode, season_number in zip(all_episodes, season_numbers)
        ]

        sorted_episodes = sorted(episode_list, key=lambda ep: (ep[2], ep[1]))

        return sorted_episodes
    
    def fetch_anime_episode_watch_api_url(self, slug, sel_ep, sel_seas):
        """Anime Bölüm Urlsini Al"""
        if not slug:
            return

        url = f"{self.base_url}/anime/{slug}/season/{sel_seas}/episode/{sel_ep}"
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        
        data = resp.json()
        for index in [3, 2, 1, 0]:
            try:
                file = data["episodeData"]["files"][index]["file"]
                return file
            except (IndexError, KeyError):
                continue
