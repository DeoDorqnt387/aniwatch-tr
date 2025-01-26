import os, time, re, requests
import subprocess
import tools

from urllib.parse import urlparse, parse_qs
from InquirerPy import inquirer, prompt
from InquirerPy.base.control import Choice

from watch import *

class anifetch:
    def __init__(self):
        # WEBSITE: https://animecix.net/
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
        try:
            search_url = f"{self.base_url}secure/search/{query}?type=&limit=20"
            data = self._get_json(search_url)
            if data and 'results' in data:
                return [
                    {'name': item.get('name'), 
                    'id': item.get('id'), 
                    'type': item.get('type'), 
                    'title_type': item.get("title_type"), 
                    'original_title': item.get("original_title")}
                    for item in data['results']
                ]
        except Exception as e:
            print(f"Error fetching anime search data: {e}")
        return []

    def fetch_anime_seasons(self, selected_id):
        """Fetch seasonal data for the specified anime ID."""
        url = f"https://mangacix.net/secure/related-videos?episode=1&season=1&titleId={selected_id}"
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
            srch_eps_data_url = f"https://mangacix.net/secure/related-videos?episode=1&season={season_index + 1}&titleId={selected_id}"
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
        except requests.RequestException as e:
            print("Error occurred while fetching watch API URL:", e)
            return []

    def fetch_anime_watch_api_url_movie(self, selected_id):
        """Fetch watch URL for a movie based on its ID."""
        url = f"https://mangacix.net/secure/titles/{selected_id}"
        json_dt = self._get_json(url)
        
        if not json_dt:
            print(f"Error: Unable to fetch JSON data from {url}")
            return None
        
        url_vid = json_dt.get("title", {}).get("videos", [{}])[0].get("url")
        
        if not url_vid:
            print(f"Error: No video URL found in JSON data from {url}")
            return None
        
        try:
            path = urlparse(url_vid).path
            embed_id = path.split("/")[2]
            api_url = f"https://{self.video_players[0]}/api/video/{embed_id}"
            video_data = self._get_json(api_url)
            
            if not video_data:
                print(f"Error: Unable to fetch JSON data from {api_url}")
                return None
            
            best_qualities = ["1080p", "720p", "480p"]
            for quality in best_qualities:
                for url_info in video_data.get('urls', []):
                    if url_info.get("label") == quality:
                        return url_info.get("url")
        except Exception as e:
            print(f"Error while fetching movie URL: {e}")
            if self.video_players[1] in url_vid:
                return url_vid + ".mp4"
        
        return None

class animecix:
    def __init__(self):
        self.base_url = "https://www.animecix.net/"
        self.current_episode_index = None
        self.selected_id = None
        self.episodes = []
        self.ftch_dt_a = anifetch()
        self.selected_website = ""
        self.current_anime_name = ""

    def display_menu(self):
        """Ana Menü Gösterimi"""
        tools.clear_screen() 
        is_movie = (
            self.episodes is None or 
            len(self.episodes) <= 1 or 
            (isinstance(self.episodes, dict) and self.episodes.get("title_type") == "movie")
        )
        
        total_episodes = (
            len(self.episodes) if isinstance(self.episodes, list) else 1
        )

        if not is_movie:
            menu_header = (f"\033[33mOynatılıyor\033[0m: {self.current_anime_name} (tr-altyazılı) | "
            f"Olabilecek en yüksek kalite | {self.current_episode_index + 1}/{total_episodes}"
            if self.current_anime_name else "")
            print(menu_header)

            questions = [
                {
                    "type": "list",
                    "name": "selection",
                    "message": 'Bir Seçenek Seçiniz',
                    "choices":  ['Şu anki Bölümü Oynat','Sonraki Bölüm','Önceki Bölüm','Bölüm Seç','Bölüm İndir','Anime Ara','Çık'],
                    "cycle": True,
                    "border": True,
                },
            ]
        else:
            menu_header = (f"\033[33mOynatılıyor\033[0m: {self.current_anime_name} (tr-altyazılı) | "
            f"Olabilecek en yüksek kalite | {self.current_episode_index + 1}"
            if self.current_anime_name else "")
            print(menu_header)

            questions = [
                {
                    "type": "list",
                    "name": "selection",
                    "message": 'Bir Seçenek Seçiniz',
                    "choices": ['Filmi İzle','Filmi İndir','Anime Ara', 'Çık'],
                    "cycle": True,
                    "border": True,
                },
            ]
        
        answers = prompt(questions)
        selected_option = answers['selection']
        return selected_option


    def select_episode(self, episodes):
        """Bölüm Seç"""
        episode_choices = [episode['name'] for episode in episodes]
        ep_questions = [
            {
                "type": "fuzzy",
                "name": "episode_selection",
                "message": "Bir Bölüm seçin:",
                "choices": episode_choices,
                "cycle": True,
                "border": True,
            }
        ]
        answers = prompt(ep_questions)
        selected_name = answers['episode_selection']
        selected_episode = next(ep for ep in episodes if ep['name'] == selected_name)
        selected_url = selected_episode['url']

        self.selected_name = selected_name
        self.selected_url = selected_url

        return selected_name, selected_url

    def handle_menu_option(self, option):
        """Menu Seçim"""
        actions = {
            'Şu anki Bölümü Oynat': lambda: tools.play_current_episode(self),
            'Sonraki Bölüm': lambda: tools.next_episode(self),
            'Önceki Bölüm': lambda: tools.previous_episode(self),
            'Bölüm Seç': lambda: tools.select_ep(self),
            'Anime Ara': self.srch_anime,
            'Bölüm İndir': self.download_episodes,
            'Çık': tools.exit_app,

            'Filmi İzle': lambda: tools.play_current_episode(self),
            'Filmi İndir': self.download_episodes,
        }
        if not isinstance(option, str):
            print(f"Invalid option type: {type(option)}")
            tools.invalid_option()
            return
        action = actions.get(option, tools.invalid_option)
        action()

    def srch_anime(self):
        """Anime Arat"""
        query = inquirer.text(message="Lütfen Bir Anime Adı Giriniz:").execute()
        tools.clear_screen()
        anime_srch_dt = self.ftch_dt_a.fetch_anime_search_data(query)
        if not anime_srch_dt:
            print("Sonuç Bulunamadı")
            return
        
        anime_choices = [f"{item['name']} [{item['original_title']}] (ID: {item['id']})" for item in anime_srch_dt]
        questions = [
            {
                "type": "fuzzy",
                "name": "anime_selection",
                "message": "Bir Anime Seçin.",
                "choices": anime_choices,
                "border": True,
                "cycle": True,
                "height": "%40",
            }
        ]
        answers = prompt(questions)
        selected_choice = answers["anime_selection"]
        match = re.match(r'(.+) \(ID: (\d+)\)', selected_choice)
        if match:
            selected_name = match.group(1)
            selected_id = match.group(2)

        self.episodes = self.ftch_dt_a.fetch_anime_episodes(selected_id)
        self.selected_id = selected_id
        
        self.current_anime_name = selected_name
        self.current_episode_index = 0

        while True:
            tools.clear_screen()
            option = self.display_menu()
            self.handle_menu_option(option)
            
    def download_episodes(self):
        """İndirilecek Bölümleri Seç ve İndir"""
        if self.episodes is None:
            download_url = self.ftch_dt_a.fetch_anime_watch_api_url_movie(self.selected_id)
            anime_name = self.current_anime_name

            base_directory = 'Animeler'
            if not os.path.exists(base_directory):
                os.makedirs(base_directory)

            anime_directory = os.path.join(base_directory, anime_name)
            if not os.path.exists(anime_directory):
                os.makedirs(anime_directory)

            if download_url:    
                file_name = f"{anime_name}.mp4"
                file_path = os.path.join(anime_directory, file_name)
                try:
                    print(f"{anime_name} İndiriliyor...")
                    subprocess.run(['yt-dlp', '--external-downloader', 'aria2c', '--external-downloader-args', '-x 16 -s 16 -k 1M','--no-warnings', '-o', file_path,download_url], check=True)
                except subprocess.CalledProcessError as e:
                    print("İndirme Sırasında Bir Hata Oluştu!", e)
            else:
                print("Geçerli Bir İndirme Urlsi Bulunamadı!", anime_name)
        else:
            episode_choices = [Choice(name=episode['name'], value=episode) for episode in self.episodes]
            ep_que=[{"type": "checkbox", "name": "episode_selection", "message": "İndirmek istediğiniz bölümleri seçin:", "choices": episode_choices, "cycle": True, "border": True}]

            answers = prompt(ep_que)                                            
            selected_episodes = answers["episode_selection"]

            base_directory = 'Animeler'
            if not os.path.exists(base_directory):
                os.makedirs(base_directory)

            for episode in selected_episodes:
                episode_name = episode['name']
                episode_url = episode['url']
                anime_name = self.current_anime_name

                anime_directory = os.path.join(base_directory, anime_name)
                if not os.path.exists(anime_directory):
                    os.makedirs(anime_directory)
                
                urls = self.ftch_dt_a.fetch_anime_watch_api_url(episode_url)

                try_best_qua = [3,2,1,0]
                if not urls or not any(urls[i].get('url') for i in try_best_qua if i < len(urls)):
                    print(f"İndirme URL'si Bulunamadı!")
                    return
                
                download_url = next((urls[index]['url'] for index in try_best_qua if index < len(urls) and urls[index].get('url')), None)
                if download_url:    
                    file_name = f"{episode_name}.mp4"
                    file_path = os.path.join(anime_directory, file_name)
                    try:
                        print(f"{episode_name} İndiriliyor...")
                        subprocess.run(['yt-dlp', '--external-downloader', 'aria2c', '--external-downloader-args', '-x 16 -s 16 -k 1M','--no-warnings', '-o', file_path,download_url], check=True)
                    except subprocess.CalledProcessError as e:
                        print("İndirme Sırasında Bir Hata Oluştu!", e)
                else:
                    print("Geçerli Bir İndirme Urlsi Bulunamadı!", episode_name)

    def play_episode(self, index):
        """Spesifik bir Bölümü Oynat"""
        if not (self.episodes and isinstance(self.episodes, list) and 0 <= index < len(self.episodes)):
            if hasattr(self, 'selected_id'):
                url = self.ftch_dt_a.fetch_anime_watch_api_url_movie(self.selected_id)
                if url:
                    open_with_video_player(url)
                else:
                    print("Film URL'si bulunamadı.")
                return

            print("Geçerli bir bölüm bulunamadı veya indeks geçersiz.")
            return

        episode = self.episodes[index]
        episode_url = episode.get('url')
        if not episode_url:
            print("Bölüm URL'si bulunamadı.")
            return

        urls = self.ftch_dt_a.fetch_anime_watch_api_url(episode_url)
        if not urls:
            print("URL'ler Bulunamadı.")
            return

        try_best_qua = [2, 1, 0]
        play_url = next((urls[idx].get('url') for idx in try_best_qua if idx < len(urls)), None)

        if play_url:
            print(f"Şu anki Bölüm: {episode['name']}")
            open_with_video_player(play_url)
        else:
            print(f"Geçerli Bir Video URL'si Bulunamadı: {episode['name']}")
