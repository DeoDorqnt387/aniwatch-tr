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
    
    def fetch_anime_seasons(self, selected_id):
        url = f"https://www.mangacix.net/secure/related-videos?episode=1&season=1&titleId={selected_id}"
        response = requests.get(url)

        if response.status_code == 200:
            try:
                json_data = response.json()

                if "videos" in json_data:
                    seasons = json_data["videos"][0]["title"]["seasons"]

                    if isinstance(seasons, list):
                        return list(range(len(seasons)))
                    else:
                        print("'seasons'ın bir liste olması gerekliydi:", type(seasons))
                        return []
                else:
                    print("'videos' ya da 'seasons' Verisi Bulunmamaktadır.")
                    return []
            except ValueError:
                print("Hatalı json Verisi.")
                return []
        else:
            print(f"İstek Hatası: {response.status_code}")
            return []

    def fetch_anime_eps(self, selected_id):
        index_of_seasons = self.fetch_anime_seasons(selected_id)

        episodes = []                                   
        for index in index_of_seasons:
            data_url = f"https://www.mangacix.net/secure/related-videos?episode=1&season={index + 1}&titleId={selected_id}"
            response = requests.get(data_url)
            response.raise_for_status()
            data = response.json()

            for item in data.get('videos', []):
                episode_name = item.get('name', 'No name field')
                episode_url = item.get('url', 'No URL field')
                episode_thumbnail = item.get('thumbnail', 'No thumbnail field')
                episodes.append({'name': episode_name, 'url': episode_url, 'thumbnail': episode_thumbnail})

        return episodes
