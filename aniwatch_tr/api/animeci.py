import time
import requests
from urllib.parse import urlparse, parse_qs

from aniwatch_tr.core import ErrorHandler, ErrorCodes, AnimeciError

error_handler = ErrorHandler()

class AnimeciAPI:
    def __init__(self):
        # WEBSITE: https://anm.cx/
        self.base_url = ["https://animecix.tv/", "https://mangacix.net"]
        self.video_players = ["tau-video.xyz", "sibnet"]
        self.headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def _get_json(self, url):
        """Fetch JSON data from the specified URL."""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_handler.log_error(
                ErrorCodes.ERROR_FETCHING_JSON_FROM, 
                original_error=e, 
                url=url, 
                raise_exception=True
            )

    def fetch_anime_search_data(self, query):
        """Fetch anime search data based on the query."""
        try:
            search_url = f"{self.base_url[0]}secure/search/{query}?type=&limit=20"
            data = self._get_json(search_url)
            if data and 'results' in data:
                return [
                    {'name': item.get('name'), 
                    'id': item.get('id'), 
                    'type': item.get('type'), 
                    'title_type': item.get("title_type")}
                    for item in data['results']
                ]
        except AnimeciError as e:
            error_handler.log_warning(f"Search işleminde hata: {e}")
            return []
        return []
    
    def fetch_anime_seasons(self, selected_id):
        """Fetch seasonal data for the specified anime ID."""
        url = f"{self.base_url[1]}/secure/related-videos?episode=1&season=1&titleId={selected_id}&videoId=637113"
        json_data = self._get_json(url)
        try: 
            if json_data and "videos" in json_data:
                videos = json_data["videos"]
                if videos:
                    seasons = videos[0].get('title', {}).get('seasons', [])
                    if isinstance(seasons, list):
                        return list(range(len(seasons)))
            return []
        except AnimeciError as e:
            error_handler.log_warning(f"Seasonal işleminde hata: {e}")
            return []
        
    def fetch_anime_episodes(self, selected_id):
        """Fetch episode data for the specified anime ID."""
        seasons = self.fetch_anime_seasons(selected_id)
        episodes = []
        seen_episode_names = set()
        try:

            for season_index in seasons:
                srch_eps_data_url = f"{self.base_url[1]}/secure/related-videos?episode=1&season={season_index + 1}&titleId={selected_id}&videoId=637113"
                data = self._get_json(srch_eps_data_url)
                if data and 'videos' in data:
                    for item in data['videos']:
                        episode_name = item.get('name', "No url field")
                        if episode_name not in seen_episode_names:
                            episode_url = item.get('url', 'No name field')
                            episodes.append({'name': episode_name, 'url': episode_url})
                            seen_episode_names.add(episode_name)
            return episodes
        except AnimeciError as e:
            error_handler.log_warning(f"Episode işleminde hata: {e}")
            return []

    def fetch_anime_stream_api_url(self, url):
        """Fetch the watch URL for a given anime URL."""
        stream_url = f"{self.base_url[0]}{url}"
        try:
            response = requests.get(stream_url, headers=self.headers, allow_redirects=True)
            response.raise_for_status()

            time.sleep(3)

            final_resp = response.url
            path = urlparse(final_resp).path
            embed_id = path.split('/')[2]
            query = urlparse(final_resp).query
            vid = parse_qs(query).get('vid', [None])[0]

            watch_url = f"https://{self.video_players[0]}/api/video/{embed_id}?vid={vid}"
            wtch_resp = requests.get(watch_url)
            wtch_resp.raise_for_status()

            urls = [{'url': item.get('url', 'No URL field')} for item in wtch_resp.json().get('urls', [])]
            return urls
        except requests.exceptions.RequestException as e:
            error_handler.log_error(
                ErrorCodes.ERROR_STREAM_URL, 
                original_error=e, 
                url=url, 
                raise_exception=True
            )
            return []
        
    ########################################################
    def fetch_anime_stream_api_url_movie(self, selected_id):
        """Fetch watch URL for a movie based on its ID."""
        url = f"{self.base_url[1]}/secure/titles/{selected_id}"
        json_dt = self._get_json(url)
        
        if not json_dt:
            error_handler.log_error(
                ErrorCodes.ERROR_MOVIE_DATA, 
                url=url,
                raise_exception=True
            )
        
        url_vid = json_dt.get("title", {}).get("videos", [{}])[0].get("url")
        
        if not url_vid:
            error_handler.log_error(
                ErrorCodes.ERROR_MOVIE_URL, 
                url=url,
                raise_exception=True
            )
        
        try:
            path = urlparse(url_vid).path
            embed_id = path.split("/")[2]
            api_url = f"https://{self.video_players[0]}/api/video/{embed_id}"
            print(api_url)
            time.sleep(5)
            video_data = self._get_json(api_url)
            
            if not video_data:
                print(f"ERR: Unable to fetch JSON data from {api_url}")
                return None
            
            best_qualities = ["1080p", "720p", "480p"]
            for quality in best_qualities:
                for url_info in video_data.get('urls', []):
                    if url_info.get("label") == quality:
                        return url_info.get("url")
        except requests.exceptions.RequestException as e:
            error_handler.log_error(
                ErrorCodes.ERROR_MOVIE_DATA, 
                original_error=e, 
                url=url, 
                raise_exception=True
            )
            return []
        
        return None