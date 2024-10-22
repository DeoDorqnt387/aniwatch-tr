import requests
import time
from urllib.parse import urlparse, parse_qs

class FetchData_a:
    def __init__(self):
        self.base_url = "https://animecix.net/"
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
        except requests.RequestException as e:
            print(f"Error fetching JSON from {url}: {e}")
            return None

    def fetch_anime_search_data(self, query):
        """Fetch anime search data based on the query."""
        search_url = f"{self.base_url}/secure/search/{query}?type=&limit=20"
        data = self._get_json(search_url)
        if data and 'results' in data:
            return [{'name': item.get('name'), 'id': item.get('id'), 'type': item.get('type')} for item in data['results']]
        return []

    def fetch_anime_seasons(self, selected_id):
        """Fetch seasonal data for the specified anime ID."""
        url = f"{self.base_url}secure/related-videos?episode=1&season=1&titleId={selected_id}"
        json_data = self._get_json(url)

        if json_data and "videos" in json_data:
            videos = json_data["videos"]
            if videos:
                seasons = videos[0].get('title', {}).get('seasons', [])
                if isinstance(seasons, list):
                    return list(range(len(seasons)))
        return []

    def fetch_anime_episodes(self, selected_id):
        """Fetch episode data for the specified anime ID."""
        seasons = self.fetch_anime_seasons(selected_id)
        episodes = []
        seen_episode_names = set()

        for season_index in seasons:
            srch_eps_data_url = f"{self.base_url}secure/related-videos?episode=1&season={season_index + 1}&titleId={selected_id}"
            data = self._get_json(srch_eps_data_url)
            if data and 'videos' in data:
                for item in data['videos']:
                    episode_name = item.get('name', "No url field")
                    if episode_name not in seen_episode_names:
                        episode_url = item.get('url', 'No name field')
                        episodes.append({'name': episode_name, 'url': episode_url})
                        seen_episode_names.add(episode_name)
        return episodes

    def fetch_anime_watch_api_url(self, url):
        """Fetch the watch URL for a given anime URL."""
        wtch_url = f"{self.base_url}{url}"
        try:
            response = requests.get(wtch_url, headers=self.headers, allow_redirects=True)
            response.raise_for_status()

            time.sleep(3)  # Avoid being flagged as a bot

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
        except requests.RequestException as e:
            print("Error occurred while fetching watch API URL:", e)
            return []

    def fetch_anime_watch_api_url_movie(self, selected_id):
        """Fetch watch URL for a movie based on its ID."""
        url = f"https://animecix.net/secure/titles/{selected_id}"
        json_dt = self._get_json(url)
        if json_dt:
            url_vid = json_dt.get("title", {}).get("videos", [{}])[0].get("url")
            if url_vid:
                try:
                    path = urlparse(url_vid).path
                    embed_id = path.split("/")[2]
                    api_url = f"https://{self.video_players[0]}/api/video/{embed_id}"
                    video_data = self._get_json(api_url)

                    # Attempt to find the best quality URL
                    best_qualities = ["1080p", "720p", "480p"]
                    for quality in best_qualities:
                        for url_info in video_data.get('urls', []):
                            if url_info.get("label") == quality:
                                return url_info.get("url")
                except Exception as e:
                    print("Error while fetching movie URL:", e)
                    if self.video_players[1] in url_vid:
                        return url_vid + ".mp4"
        return None

class FetchData_b:
    def __init__(self):
        self.base_url = "https://api.openani.me"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def fetch_anime_search_data(self, query):
        """Fetch anime search data based on the query."""
        search_url = f"{self.base_url}/anime/search?q={query}"
        data = self._get_json(search_url)
        if data:
            return [{'name': anime.get('english'), 'slug': anime.get('slug')} for anime in data]
        return []

    def fetch_anime_seasons_data(self, slug):
        """Fetch anime season data based on the slug."""
        url = f"{self.base_url}/anime/{slug}"
        data = self._get_json(url)
        if data:
            seasons_count = data.get("numberOfSeasons", 0)
            malID = data.get("malID")
            type = data.get("type")

            return seasons_count, slug, malID
        return 0, slug, None

    def fetch_anime_season_episodes(self, slug):
        """Fetch all episodes for each season of the anime."""
        season_count, slug, malID = self.fetch_anime_seasons_data(slug)
        if not season_count:
            print("No seasons found.")
            return []

        all_episodes = []
        season_numbers = []

        for season in range(1, season_count + 1):
            url = f"{self.base_url}/anime/{slug}/season/{season}"
            data = self._get_json(url)
            if data:
                episodes = data.get("season", {}).get("episodes", [])
                season_number = data["season"]["season_number"]

                all_episodes.extend(episodes)
                season_numbers.extend([season_number] * len(episodes))

        return sorted(
            [(episode.get("name"), episode.get("episodeNumber"), season_number)
             for episode, season_number in zip(all_episodes, season_numbers)],
            key=lambda ep: (ep[2], ep[1])
        )

    def fetch_anime_episode_watch_api_url(self, slug, sel_ep, sel_seas):
        """Fetch the watch URL for a specific episode."""
        if not slug:
            print("No slug provided.")
            return None

        url = f"{self.base_url}/anime/{slug}/season/{sel_seas}/episode/{sel_ep}"
        data = self._get_json(url)
        if data and "episodeData" in data:
            for index in range(3, -1, -1):
                try:
                    return data["episodeData"]["files"][index]["file"]
                except (IndexError, KeyError):
                    continue
        return None

    def _get_json(self, url):
        """Fetch JSON data from the specified URL."""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching JSON from {url}: {e}")
            return None
