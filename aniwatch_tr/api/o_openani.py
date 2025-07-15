#########################
## GEREKSİZ KOD YIĞINI ##
#########################
import requests

class openfetch:
    def __init__(self):
        self.base_url = "https://api.openani.me"
        self.player = "https://de2---vn-t9g4tsan-5qcl.yeshi.eu.org"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            "Origin": "https://openani.me",
            "Referer": "https://openani.me",
            "Accept": "application/json",
        })

    def fetch_anime_search_data(self, query):
        url = f"{self.base_url}/anime/search?q={query}"
        return self.get_json(url)

    def fetch_anime_seasons_data(self, slug):
        url = f"{self.base_url}/anime/{slug}"
        return self.get_json(url)

    def fetch_anime_season_episodes(self, slug):
        seasons_data = self.fetch_anime_seasons_data(slug)
        if not seasons_data:
            print("No seasons data found.")
            return []

        seasons_count = seasons_data.get("numberOfSeasons", 0)
        all_episodes = []
        for season_num in range(1, seasons_count + 1):
            url = f"{self.base_url}/anime/{slug}/season/{season_num}"
            data = self.get_json(url)
            if data:
                episodes = data.get("season", {}).get("episodes", [])
                season_number = data.get("season", {}).get("season_number", season_num)
                for ep in episodes:
                    all_episodes.append((ep.get("name"), ep.get("episodeNumber"), season_number))
        return sorted(all_episodes, key=lambda x: (x[2], x[1]))

    def fetch_anime_episode_stream_api_url(self, slug, season, episode):
        url = f"{self.base_url}/anime/{slug}/season/{season}/episode/{episode}"
        data = self.get_json(url)
        if data and "episodeData" in data:
            files = data["episodeData"].get("files", [])
            if files:
                # En yüksek çözünürlük dosyasını seç (örnek olarak ilk dosya)
                file_entry = files[0]
                file_path = file_entry.get("file")
                if file_path:
                    # Player URL + dosya yolu
                    final_url = f"{self.player}/videos/{file_path}"
                    return final_url
        return None

    def get_json(self, url):
        try:
            resp = self.session.get(url)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            print(f"Error fetching JSON from {url}: {e}")
            if resp is not None:
                print("Response status:", resp.status_code)
                print("Response content:", resp.text)
            return None


class OpenaniAPI:
    def __init__(self):
        self.client = openfetch()

    def fetch_anime_search_data(self, query):
        data = self.client.fetch_anime_search_data(query)
        if data:
            return [{'name': anime.get('english'), 'slug': anime.get('slug')} for anime in data]
        return []

    def fetch_anime_seasons(self, slug):
        seasons_data = self.client.fetch_anime_seasons_data(slug)
        seasons_count = seasons_data.get("numberOfSeasons", 1) if seasons_data else 1
        return [{"season_number": i} for i in range(1, seasons_count + 1)]

    def fetch_anime_episodes(self, slug):
        episodes = self.client.fetch_anime_season_episodes(slug)
        return [
            {
                "name": name,
                "episodeNumber": ep_num,
                "season_number": season_num,
                "url": f"{slug}|{season_num}|{ep_num}"
            }
            for name, ep_num, season_num in episodes
        ]

    def fetch_anime_stream_api_url(self, url_string):
        try:
            slug, season, episode = url_string.split("|")
            stream_url = self.client.fetch_anime_episode_stream_api_url(slug, season, episode)
            print(f"Stream URL: {stream_url}")
            import time
            time.sleep(1)
            if stream_url:
                return [{"url": stream_url}]
            return []
        except Exception as e:
            print("Stream API error:", e)
            return []