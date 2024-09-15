import requests
import time

from urllib.parse import urlparse, parse_qs

class FetchData:
    def __init__(self):
        self.base_url = "https://www.mangacix.net/"
        self.video_players = ["tau-video.xyz", "sibnet"]
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    def _get_json(self, url):
        """Jon Verisini Al"""
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def fetch_anime_srch_dt(self, query):
        """Arama Verisi"""
        search_url = f"{self.base_url}secure/search/{query}?limit=20"
        data = self._get_json(search_url)
        return [{'name': item.get('name'), 'id': item.get('id'), 'type': item.get('type')} for item in data.get('results', [])]

    def fetch_anime_srch_seasons(self, selected_id):
        """Sezonsal Veri"""
        url = f"{self.base_url}secure/related-videos?episode=1&season=1&titleId={selected_id}"
        json_data = self._get_json(url)

        videos = json_data.get("videos", [])

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
