"""BELKİ BİR GÜN"""
import os, subprocess, time, re

from InquirerPy import inquirer, prompt
from InquirerPy.base.control import Choice

from fetch import FetchData_a
from watch import WatchAnime
from openani import Openani

class animecix:
    def __init__(self, use_vlc=False, resolution="1080p"):
        self.base_url = "https://www.mangacix.net/"
        self.current_episode_index = None
        self.selected_id = None
        self.episodes = []
        self.ftch_dt_a = FetchData_a()
        self.wtch_dt = WatchAnime(use_vlc=use_vlc)
        self.selected_website = ""
        self.current_anime_name = ""
        self.resolution = resolution

    def clear_screen(self):
        """Terminal Ekranını Temizle"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_website_selection_thing(self):
        """Website Seçim Penceresi"""
        choices= ["AnimeciX (ID: 856)", "Openani.me (ID: 525)"]
        l = [
            {
                "type":"list",
                "name":"website_selection",
                "message": "Bir Website Seçin.",
                "choices": choices,
                "border": True,
                "cycle":True,
            }
        ]
        l = prompt(l)
        selected_choices = l["website_selection"]
        print(selected_choices)
        return selected_choices

    def play_current_episode(self, quality=None):
        """Şu anki Bölümü Oynat"""
        if self.current_episode_index is not None:
            self.play_episode(self.current_episode_index, quality)
        else:
            print("Bölüm Seçilmedi!")
            time.sleep(0.8)

    def next_episode(self):
        """Siradaki Bölüme Git"""
        if self.current_episode_index is not None and self.current_episode_index < len(self.episodes) -1:
            self.current_episode_index += 1
        else:
            print("Sonraki Bölüm Yok!")
            time.sleep(0.8)
    
    def previous_episode(self):
        """Önceki Bölüme Git"""
        if self.current_episode_index is not None and self.current_episode_index > 0:
            self.current_episode_index -= 1
        else:
            print("Önceki Bölüm Yok!")
            time.sleep(0.8)

    def select_ep(self):
        """Bölüm Seç ve Oynat(?)"""
        selected_name, selected_url = self.select_episode(self.episodes)
        self.current_episode_index = next(i for i, ep in enumerate(self.episodes) if ep['name'] == selected_name)
            
    def invalid_option(self):
        """Geçersiz veri"""
        print("Geçersiz bir seçenek girdiniz. Lütfen geçerli bir seçenek giriniz.")
        time.sleep(1)

    def exit_app(self):
        """Çık"""
        print("Çıkış yapılıyor...")
        time.sleep(0.6)
        exit()

    def display_menu(self):
        """Ana Menü Gösterimi"""
        self.clear_screen() 
        if self.current_anime_name and self.current_episode_index is not None and self.episodes:
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
            menu_header = (f"\033[33mOynatılıyor\033[0m: {self.current_anime_name} (tr-altyazılı) | "
                        f"1080p | {self.current_episode_index + 1}/{len(self.episodes)}"
                        if self.current_anime_name else "")
            
            print(menu_header)

            answers = prompt(questions)
            selected_option = answers['selection']
            return selected_option
        else:
            menu_header = (f"\033[33mOynatılıyor\033[0m: {self.current_anime_name} (tr-altyazılı) | "
                f"1080p | {self.current_episode_index + 1}"
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
            'Şu anki Bölümü Oynat': self.play_current_episode,
            'Sonraki Bölüm': self.next_episode,
            'Önceki Bölüm': self.previous_episode,
            'Bölüm Seç': self.select_ep,
            'Anime Ara': self.srch_anime,
            'Bölüm İndir': self.download_episodes,
            'Çık': self.exit_app,

            'Filmi İzle': self.play_current_episode,
            'Filmi İndir': self.download_episodes,
        }
        if not isinstance(option, str):
            print(f"Invalid option type: {type(option)}")
            self.invalid_option()
            return
        action = actions.get(option, self.invalid_option)
        action()

    def srch_anime(self):
        """Anime Arat"""
        query = inquirer.text(message="Lütfen Bir Anime Adı Giriniz:").execute()
        self.clear_screen()
        anime_srch_dt = self.ftch_dt_a.fetch_anime_srch_dt(query)
        if not anime_srch_dt:
            print("Sonuç Bulunamadı")
            return
        
        anime_choices = [f"{item['name']} (ID: {item['id']})" for item in anime_srch_dt]
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

        self.episodes = self.ftch_dt_a.fetch_anime_srch_eps(selected_id)
        self.selected_id = selected_id 
        
        self.current_anime_name = selected_name
        self.current_episode_index = 0

        while True:
            self.clear_screen()
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

    def play_episode(self, index, quality=None):
        """Spesifik bir Bölümü Oynat"""
        if not (self.episodes and isinstance(self.episodes, list) and 0 <= index < len(self.episodes)):
            if hasattr(self, 'selected_id'):
                url = self.ftch_dt_a.fetch_anime_watch_api_url_movie(selected_id=self.selected_id)
                self.wtch_dt.open_with_video_player(url)
            else:
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

        quality_map = {1080: 2, 720: 1, 480: 0}
        try_best_qua = [quality_map.get(abs(quality), 2)] if quality else [2, 1, 0]

        play_url = next((urls[idx].get('url') for idx in try_best_qua if idx < len(urls)), None)

        if play_url:
            print(f"Şu anki Bölüm: {episode['name']}")
            self.wtch_dt.open_with_video_player(play_url)
        else:
            print(f"Geçerli Bir Video URL'si Bulunamadı: {episode['name']}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Anime oynatıcı.")
    parser.add_argument("-v", "--vlc", action="store_true", help="VLC ile video oynat")
    parser.add_argument("-r", "--resolution", type=str, choices=["1080p", "720p", "480p"], default="1080p", help="Oynatma çözünürlüğü")
    args = parser.parse_args()

    use_vlc = args.vlc
    resolution = args.resolution
    app = animecix(use_vlc=use_vlc)
    openani = Openani()
    selection = app.display_website_selection_thing()
    if selection == "AnimeciX (ID: 856)":
        app.srch_anime()
    else:
        openani.srch_anime()
