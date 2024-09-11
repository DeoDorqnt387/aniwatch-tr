#!/usr/bin/env python3
import os
import inquirer
import requests
import subprocess

from fetch import fetch_data
from watch import watch_anime

class GetAnimeApp:
    def __init__(self, use_vlc=False):
        self.base_url = "https://www.mangacix.net/"
        self.current_episode_index = None 
        self.episodes = []
        self.current_anime_name = ""
        self.use_vlc = use_vlc
        self.selected_name = ""
        self.selected_url = ""

    def select_option(self, choices, message):
        questions = [
            inquirer.List('selection',
                        message=message,
                        choices=choices,
                        ),
        ]
        answers = inquirer.prompt(questions)
        return answers["selection"]

    def select_anime(self, anime_data):
        choices = [f"{item['name']} (ID: {item['id']})" for item in anime_data]
        selected_choice = self.select_option(choices, "Bir anime seçin")
        selected_name, selected_id = selected_choice.split(' (ID: ')
        selected_id = selected_id.rstrip(')')
        return selected_name, selected_id

    def select_episode(self, episodes):
        episode_choices = [episode['name'] for episode in episodes]
        selected_name = self.select_option(episode_choices, "Bir bölüm seçin")
        
        selected_episode = next(ep for ep in episodes if ep['name'] == selected_name)
        selected_url = selected_episode['url']

        self.selected_name = selected_name
        self.selected_url = selected_url

        return selected_name, selected_url

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        self.clear_screen() 
        
        menu_choices = [
            'Şu anki Bölümü Oynat',
            'Sonraki Bölüm',
            'Önceki Bölüm',
            'Bölüm Seç',
            'Bölümü İndir',
            'Anime Ara',
            'Çık'
        ]
        
        print(f"Oynatılıyor: {self.current_anime_name} (tr-altyazılı) | 1080p | {self.current_episode_index + 1}/{len(self.episodes)}" if self.current_anime_name else "")
        option = self.select_option(menu_choices, "Bir seçenek giriniz")
        return option

    def handle_menu_option(self, option):
        if option == 'Şu anki Bölümü Oynat':
            if self.current_episode_index is not None:
                self.play_episode(self.current_episode_index)
            else:
                print("Henüz bir bölüm seçilmedi.")
        elif option == 'Sonraki Bölüm':
            self.next_episode()
        elif option == 'Önceki Bölüm':
            self.previous_episode()
        elif option == 'Bölüm Seç':
            self.select_and_play_episode()
        elif option == 'Anime Ara':
            self.search_anime()
        elif option == 'Bölümü İndir':
            self.download_episode()
        elif option == 'Çık':
            print("Çıkılıyor.")
            exit()
        else:
            print("Geçersiz seçenek.")

    def next_episode(self):
        if self.current_episode_index is not None and self.current_episode_index < len(self.episodes) - 1:
            self.current_episode_index += 1
            #self.play_episode(self.current_episode_index)
        else:
            print("Sonraki bölüm yok.")

    def previous_episode(self):
        if self.current_episode_index is not None and self.current_episode_index > 0:
            self.current_episode_index -= 1
            #self.play_episode(self.current_episode_index)
        else:
            print("Önceki bölüm yok.")

    def select_and_play_episode(self):
        selected_name, selected_url = self.select_episode(self.episodes)
        self.current_episode_index = next(i for i, ep in enumerate(self.episodes) if ep['name'] == selected_name)
        #self.play_episode(self.current_episode_index)

    def search_anime(self):
        query = input("Lütfen bir anime adı giriniz: ")
        fetch_dt = fetch_data()
        anime_data = fetch_dt.fetch_anime_data(query)

        if not anime_data:
            print("Sonuç bulunamadı.")
            return
        
        selected_name, selected_id = self.select_anime(anime_data)
        self.episodes = fetch_dt.fetch_anime_eps(selected_id=selected_id)
        if self.episodes:
            self.current_anime_name = selected_name
            self.current_episode_index = 0
            while True:
                self.clear_screen()
                option = self.display_menu()
                self.handle_menu_option(option)
        else:
            print("Bölüm bilgileri bulunamadı.")

    def download_episode(self):
        if self.current_episode_index is not None:
            episode_name = self.episodes[self.current_episode_index]['name']
            episode_url = self.episodes[self.current_episode_index]['url']
            anime_name = self.current_anime_name

            base_directory = 'Animeler'
            if not os.path.exists(base_directory):
                os.makedirs(base_directory)

            anime_directory = os.path.join(base_directory, anime_name)
            if not os.path.exists(anime_directory):
                os.makedirs(anime_directory)

            watch_anime_instance = watch_anime(use_vlc=self.use_vlc)
            urls = watch_anime_instance.fetch_anime_api_watch_url(episode_url)

            url_indices_to_try = [3, 2, 1, 0]
            if not urls or not any(urls[i].get('url') for i in url_indices_to_try if i < len(urls)):
                print("İndirme URL'si bulunamadı.")
                return

            download_url = None
            for index in url_indices_to_try:
                if index < len(urls) and urls[index].get('url'):
                    download_url = urls[index]['url']
                    break

            if download_url:
                file_name = f"{episode_name}.mp4"
                file_path = os.path.join(anime_directory, file_name)

                try:
                    print(f"{episode_name} indiriliyor...")

                    subprocess.run(['yt-dlp', '-o', file_path, download_url], check=True)
                    print(f"Bölüm başarıyla indirildi: {file_path}")
                except subprocess.CalledProcessError as e:
                    print(f"İndirme sırasında bir hata oluştu: {e}")
            else:
                print("İndirme URL'si bulunamadı.")
        else:
            print("İndirilmesi gereken bir bölüm seçilmedi.")

    def play_episode(self, index):
        episode = self.episodes[index]
        print(f"Oynatılan bölüm: {episode['name']}")
        url = watch_anime(use_vlc=self.use_vlc).fetch_anime_api_watch_url(episode['url'])
        watch_anime(use_vlc=self.use_vlc).anime_watch(url)

def main(): 
    import argparse

    parser = argparse.ArgumentParser(description='Yardım Merkezi')
    parser.add_argument('-v', '--vlc', action='store_true', help='VLC kullanarak oynat')
    args = parser.parse_args()

    app = GetAnimeApp(use_vlc=args.vlc)
    query = input("Lütfen bir anime adı giriniz: ")
    fetch_dt = fetch_data()
    anime_data = fetch_dt.fetch_anime_data(query)

    if not anime_data:
        print("Sonuç bulunamadı.")
        return
    
    selected_name, selected_id = app.select_anime(anime_data)

    app.episodes = fetch_dt.fetch_anime_eps(selected_id=selected_id)
    if app.episodes:
        app.current_anime_name = selected_name
        app.current_episode_index = 0           
        
        while True:
            app.clear_screen()
            option = app.display_menu()
            app.handle_menu_option(option)
    else:
        print("Bölüm bilgileri bulunamadı.")

if __name__ == "__main__":
    main()  
