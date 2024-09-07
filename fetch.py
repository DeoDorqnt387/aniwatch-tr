import requests

class fetch_data:
    def __init__(self):
        self.base_url = "https://www.mangacix.net/"

    def fetch_anime_data(self, query):
        search_url = f"{self.base_url}secure/search/{query}?limit=20"
        response = requests.get(search_url)
        response.raise_for_status()
        data = response.json()
        return [
            {'name': item.get('name', 'No name field'), 'id': item.get('id', 'No ID field')}
            for item in data.get('results', [])
        ]

    def fetch_anime_eps(self, selected_id):
        data_url = f"https://www.mangacix.net/secure/related-videos?episode=1&season=1&titleId={selected_id}"
        response = requests.get(data_url)
        response.raise_for_status()
        data = response.json()

        episodes = []
        for item in data.get('videos', []):  # 'videos' anahtarını kullanarak verileri al
            episode_name = item.get('name', 'No name field')
            episode_url = item.get('url', 'No URL field')
            episodes.append({'name': episode_name, 'url': episode_url})

        return episodes