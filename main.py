#!/usr/bin/env python3
import os
import inquirer
import requests

from fetch import fetch_data
from watch import watch_anime

class GetAnimeApp:
    def __init__(self):
        self.base_url = "https://www.mangacix.net/"
        self.current_episode_index = None  # Şu anki bölümün indeksini takip eder
        self.episodes = []  # Bölüm listesini saklar

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
        
        # Seçilen bölüm adını kullanarak URL'yi bul
        selected_episode = next(ep for ep in episodes if ep['name'] == selected_name)
        selected_url = selected_episode['url']
        
        return selected_name, selected_url

    def clear_screen(self):
        # Ekranı temizlemek için uygun komutu çalıştırır
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        self.clear_screen()  # Ekranı temizle
        
        menu_choices = [
            'Şu anki Bölümü Oynat',
            'Sonraki Bölüm',
            'Önceki Bölüm',
            'Bölüm Seç',
            'Bölümü İndir',
            'Anime Ara',
            'Çık'
        ]
        
        print(f"\nOynatılıyor: {self.current_anime_name} (tr-altyazılı) | 1080p | {self.current_episode_index + 1}/{len(self.episodes)}" if self.current_anime_name else "")
        option = self.select_option(menu_choices, "Bir seçenek giriniz:")
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
        elif option == 'Bölüm İndir':
            self.download_episode()
        elif option == 'Çık':
            print("Çıkılıyor.")
            exit()
        else:
            print("Geçersiz seçenek.")

    def next_episode(self):
        if self.current_episode_index is not None and self.current_episode_index < len(self.episodes) - 1:
            self.current_episode_index += 1
            self.play_episode(self.current_episode_index)
        else:
            print("Sonraki bölüm yok.")

    def previous_episode(self):
        if self.current_episode_index is not None and self.current_episode_index > 0:
            self.current_episode_index -= 1
            self.play_episode(self.current_episode_index)
        else:
            print("Önceki bölüm yok.")

    def select_and_play_episode(self):
        selected_name, selected_url = self.select_episode(self.episodes)
        self.current_episode_index = next(i for i, ep in enumerate(self.episodes) if ep['name'] == selected_name)
        self.play_episode(self.current_episode_index)

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
                self.clear_screen()  # Ekranı temizle
                option = self.display_menu()
                self.handle_menu_option(option)
        else:
            print("Bölüm bilgileri bulunamadı.")

    def download_episode(self):
        if self.current_episode_index is not None:
            episode = self.episodes[self.current_episode_index]
            episode_name = episode['name']
            download_url = episode['download_url']  # Bölümün indirme URL'sini al

            print(f"{episode_name} bölümü indiriliyor...")

            # İndirilen dosyayı kaydetme işlemi
            response = requests.get(download_url, stream=True)
            if response.status_code == 200:
                file_name = f"{episode_name}.mp4"  # Dosya adını uygun şekilde ayarlayın
                with open(file_name, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                print(f"Bölüm başarıyla indirildi: {file_name}")
            else:
                print("İndirme sırasında bir hata oluştu.")
        else:
            print("İndirilmesi gereken bir bölüm seçilmedi.")

    def play_episode(self, index):
        episode = self.episodes[index]
        print(f"Oynatılan bölüm: {episode['name']}")
        url = watch_anime().fetch_anime_api_watch_url(episode['url'])
        watch_anime().anime_watch(url)

    def main(self):
        fetch_dt = fetch_data()
        anime_wtch = watch_anime()
        
        query = input("Lütfen bir anime adı giriniz: ")
        anime_data = fetch_dt.fetch_anime_data(query)

        if not anime_data:
            print("Sonuç bulunamadı.")
            return
        
        selected_name, selected_id = self.select_anime(anime_data)
        
        self.episodes = fetch_dt.fetch_anime_eps(selected_id=selected_id)
        if self.episodes:
            self.current_anime_name = selected_name
            self.current_episode_index = 0
            
            # Menü döngüsünü başlat
            while True:
                self.clear_screen()  # Ekranı temizle
                option = self.display_menu()
                self.handle_menu_option(option)
        else:
            print("Bölüm bilgileri bulunamadı.")

if __name__ == "__main__":
    app = GetAnimeApp()
    app.main()
