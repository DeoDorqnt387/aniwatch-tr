import subprocess, os, time, requests, tools

from urllib.parse import urlparse, parse_qs
from InquirerPy import inquirer, prompt
from InquirerPy.base.control import Choice
from watch import *

class FetchData_b:
    def __init__(self):
        # WEBSITE: https://openani.me/
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

class Openani:
    def __init__(self):
        self.ftch_dt_b = FetchData_b()
        self.episodes = []
        self.player = "https://tp1---av-u0g3jyaa-8gcu.oceanicecdn.xyz"
        self.slug = ""
        self.episode_index = 0
        self.selected_name = ""
        self.current_anime_name = ""
        self.current_episode_index = None

    def select_ep(self):
        """Bölüm Seç"""
        selected_episode = self.select_episode(self.episodes)
        self.current_episode_index = next((i for i, ep in enumerate(self.episodes) if ep == selected_episode),None)
                
    def select_episode(self, episodes):
        """Bölüm Seç"""
        episode_choices = [
            Choice(name=f"{episode[0]} (Sezon {episode[2]}, Bölüm {episode[1]})", value=episode)
            for episode in self.episodes
        ]
        selected_name = prompt([{
            "type": "fuzzy",
            "name": "episode_selection",
            "message": "Bir Bölüm seçin:",
            "choices": episode_choices,
            "cycle": True,
            "border": True,
        }])['episode_selection']

        self.selected_name = selected_name
        return selected_name

    
    def display_menu(self):
        """Ana Menü Gösterimi"""
        tools.clear_screen() 
        print(f"\033[33mOynatılıyor\033[0m: {self.current_anime_name} (tr-altyazılı) | {self.current_episode_index + 1}/{len(self.episodes)}")
        
        selected_option = prompt([{
            "type": "list",
            "name": "selection",
            "message": 'Bir Seçenek Seçiniz',
            "choices": ['Şu anki Bölümü Oynat', 'Sonraki Bölüm', 'Önceki Bölüm', 'Bölüm Seç', 'Bölüm İndir', 'Anime Ara', 'Çık'],
            "cycle": True,
            "border": True,
        }])['selection']
        
        return selected_option

    def handle_menu_option(self, option):
        """Menu Seçim"""
        actions = {
            'Şu anki Bölümü Oynat': lambda: tools.play_current_episode(self),
            'Sonraki Bölüm': lambda: tools.next_episode(self),
            'Önceki Bölüm': lambda: tools.previous_episode(self),
            'Bölüm Seç': lambda: tools.select_ep(self),
            'Anime Ara': self.srch_anime,
            'Bölüm İndir': self.download_eps,
            'Çık': tools.exit_app,
        }
        
        actions.get(option, tools.invalid_option)() if isinstance(option, str) else tools.invalid_option()

    def srch_anime(self):
        """Anime Arat"""
        query = inquirer.text(message="Lütfen Bir Anime Adı Giriniz: ").execute()
        results = self.ftch_dt_b.fetch_anime_search_data(query)

        selected_name = prompt([{
            "type": "fuzzy",
            "name": "anime_selection",
            "message": "Bir Anime Seçin.",
            "choices": [anime["name"] for anime in results],
            "border": True,
            "cycle": True,
            "height": "%40",
        }])["anime_selection"]

        self.slug = next(anime["slug"] for anime in results if anime["name"] == selected_name)
        self.current_anime_name, self.current_episode_index = selected_name, 0
        self.episodes = self.ftch_dt_b.fetch_anime_season_episodes(self.slug)

        while True:
            tools.clear_screen()
            self.handle_menu_option(self.display_menu())

        #return self.current_anime_name, self.slug

    def download_eps(self):
        """İndirilecek Bölümleri Seç ve İndir"""
        if self.episodes is None or not self.episodes:
            print("İndirilecek bölüm bulunamadı.")
            return

        episode_choices = [
            Choice(name=f"{episode[0]} (Sezon {episode[2]}, Bölüm {episode[1]})", value=episode)
            for episode in self.episodes
        ]

        ep_que = [{
            "type": "checkbox",
            "name": "episode_selection",
            "message": "İndirmek istediğiniz bölümleri seçin:",
            "choices": episode_choices,
            "cycle": True,
            "border": True
        }]

        answers = prompt(ep_que)
        selected_episodes = answers["episode_selection"]

        base_directory = 'Animeler'
        os.makedirs(base_directory, exist_ok=True)

        anime_directory = os.path.join(base_directory, self.current_anime_name)
        os.makedirs(anime_directory, exist_ok=True)

        # Seçilen her bölüm için indirme işlemini yap
        for episode in selected_episodes:
            episode_name, episode_number, season_number = episode
            results = self.ftch_dt_b.fetch_anime_episode_watch_api_url(self.slug, sel_ep=episode_number, sel_seas=season_number)
            final_url_result = f"{self.player}/animes/{self.slug}/{season_number}/{results}"

            if results:
                file_name = f"{episode_name}.mp4"
                file_path = os.path.join(anime_directory, file_name)
                try:
                    print(f"{episode_name} İndiriliyor...")
                    subprocess.run(['yt-dlp', '--external-downloader', 'aria2c', '--external-downloader-args', '-x 16 -s 16 -k 1M', '--no-warnings', '-o', file_path,final_url_result], check=True)
                except subprocess.CalledProcessError as e:
                    print("İndirme Sırasında Bir Hata Oluştu!", e)
            else:
                print("Geçerli Bir İndirme URL'si Bulunamadı!", episode_name)

    def play_episode(self,episode_index):
        """Spesifik bir Bölümü Oynat"""
        ## https://tp1---av-u0g3jyaa-8gcu.oceanicecdn.xyz/animes/otonari-no-tenshi-sama-ni-itsunomanika-dame-ningen-ni-sareteita-ken/1/11-7081163395176599553-720p.mp4
        self.episode_index = episode_index
        episode_name, episode_number, season_number = self.episodes[self.episode_index]
        results = self.ftch_dt_b.fetch_anime_episode_watch_api_url(self.slug, sel_ep=episode_number,sel_seas=season_number)
        print("Veri Çıkarılıyor...") 

        open_with_video_player(f"{self.player}/animes/{self.slug}/{season_number}/{results}")

        

