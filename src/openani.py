"""BELKİ BİR GÜN"""
import subprocess, os, time, re

from InquirerPy import inquirer, prompt
from InquirerPy.base.control import Choice

from fetch import FetchData_b
from watch import WatchAnime

class Openani:
    def __init__(self):
        self.ftch_dt_b = FetchData_b()
        self.watch = WatchAnime()
        self.episodes = []
        self.player = "https://tp1---av-u0g3jyaa-8gcu.oceanicecdn.xyz"
        self.slug = ""
        self.episode_index = 0
        self.selected_name = ""
        self.current_anime_name = ""
        self.current_episode_index = 0

    def play_current_episode(self, quality=None):
        """Şu anki Bölümü Oynat"""
        if self.current_episode_index is not None:
            self.play_episode(self.current_episode_index)
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

    def clear_screen(self):
        """Terminal Ekranını Temizle"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def invalid_option(self):
        """Geçersiz veri"""
        print("Geçersiz bir seçenek girdiniz. Lütfen geçerli bir seçenek giriniz.")
        time.sleep(1)

    def exit_app(self):
        """Çık"""
        print("Çıkış yapılıyor...")
        time.sleep(0.6)
        exit()

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
        self.clear_screen() 
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
            'Şu anki Bölümü Oynat': self.play_current_episode,
            'Sonraki Bölüm': self.next_episode,
            'Önceki Bölüm': self.previous_episode,
            'Bölüm Seç': self.select_ep,
            'Anime Ara': self.srch_anime,
            'Bölüm İndir': self.download_eps,
            'Çık': self.exit_app,
        }
        
        actions.get(option, self.invalid_option)() if isinstance(option, str) else self.invalid_option()

    def srch_anime(self):
        """Anime Arat"""
        query = inquirer.text(message="Lütfen Bir Anime Adı Giriniz: ").execute()
        results = self.ftch_dt_b.fetch_anime_srch_data(query)

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
        self.episodes = self.ftch_dt_b.fetch_anime_seasons_episodes(self.slug)

        while True:
            self.clear_screen()
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

        self.watch.open_with_video_player(f"{self.player}/animes/{self.slug}/{season_number}/{results}")

        

if __name__ == "__main__":
    open = Openani()
    open.srch_anime()
