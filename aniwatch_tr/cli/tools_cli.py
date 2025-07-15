import os
import yt_dlp
from tqdm import tqdm

from os import system, name
from prompt_toolkit import styles

from aniwatch_tr.core.config import get_download_folder,load_config
from pathlib import Path
from rich import print as rprint
from rich.panel import Panel
from rich.console import Group
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    SpinnerColumn,
    TimeElapsedColumn
)

prompt_style = styles.Style([
    ('qmark',        'fg:#ffe198 bold'),       # Tatlı sarı soru işareti
    ('question',     'fg:#fefefe bold'),       # Beyazımsı açık soru metni
    ('answer',       'fg:#ffd166 bold'),       # Sıcak pastel sarı cevap
    ('pointer',      'fg:#ffe198 bold'),       # Aynı sarıdan ok
    ('highlighted',  'fg:#ffd166 bold'),       # Seçenek vurgusu
    ('selected',     'fg:#fefefe bold'),       # Seçili metin (arka plan yok)
    ('separator',    'fg:#aaaaaa'),            # Açık gri ayraç
    ('instruction',  'fg:#ffe198 italic'),     # Açıklama, sarı italic
    ('text',         'fg:#eeeeee'),            # Açık gri ana metin
    ('disabled',     'fg:#888888 italic'),     # Pasif itemler
])

def clear():
    system('cls' if name == 'nt' else 'clear')

def Status(message, hide=True, spinner="dots", color="yellow"):
    """    
    Args:
        message (str): Gösterilecek mesaj
        hide (bool): Bitince gizle
        spinner (str): Spinner tipi (ör. dots, line, moon, earth, etc.)
        color (str): Yazı ve bar rengi
        
    Returns:
        Progress: Rich Progress instance
    """
    progress = Progress(
        SpinnerColumn(spinner, style=color),
        TextColumn(f"[{color} bold]{message}"),
        BarColumn(bar_width=40, style="black", complete_style=f"{color}"),
        TimeElapsedColumn(),
        transient=hide
    )
    progress.add_task(message, total=None)
    return progress

class Download:
    def __init__(self, anime_api):
        self.api = anime_api
        self.anime_name = None
        self.anime_id = None
        self.episodes = None
        self.current_progress = None

    def setup_anime(self, anime_name, anime_id, episodes=None):
        """Anime bilgilerini ayarla"""
        self.anime_name = anime_name
        self.anime_id = anime_id
        self.episodes = episodes
    def get_download_folder():
        config = load_config()
        folder = config.get("download_folder")
        return folder
    
    def _create_directory(self, anime_name):
        custom_folder = get_download_folder()
        
        base_path = Path(custom_folder) if custom_folder else Path.home() / "Desktop"
        anime_directory = base_path / "Animeler" / anime_name
        anime_directory.mkdir(parents=True, exist_ok=True)
        return str(anime_directory)

    def _progress_hook(self, d):
        if self.current_progress is None:
            return

        status = d['status']
        
        if status == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_bytes = d.get('downloaded_bytes', 0)
            
            if total_bytes:
                if abs(downloaded_bytes - getattr(self, 'last_bytes', 0)) > (total_bytes * 0.01):
                    if self.current_progress.total != total_bytes:
                        self.current_progress.total = total_bytes
                    
                    self.current_progress.n = downloaded_bytes
                    
                    speed = d.get('speed', 0)
                    speed_mbps = (speed / (1024 * 1024)) if speed else 0
                    
                    self.current_progress.set_postfix({
                        'Speed': f'{speed_mbps:.1f} MB/s'
                    })
                    
                    self.current_progress.refresh()
                    self.last_bytes = downloaded_bytes
            else:
                downloaded_mb = downloaded_bytes / (1024 * 1024)
                self.current_progress.set_description(f"İndiriliyor... {downloaded_mb:.1f} MB")
                self.current_progress.refresh()
        
        elif status == 'finished':
            if self.current_progress is not None:
                self.current_progress.set_description("Tamamlandı")
                self.current_progress.refresh()
        
        elif status == 'error':
            if self.current_progress is not None:
                self.current_progress.set_description("Hata")
                self.current_progress.refresh()

    def _download_video(self, url, file_path, name):
        """Video indirme fonksiyonu"""
        if not url:
            print(f"Geçerli URL bulunamadı: {name}")
            return False

        ydl_opts = {
            'outtmpl': file_path,
            'progress_hooks': [self._progress_hook],
            'quiet': True,
            'no_warnings': True,
            'noprogress': True
        }
        
        desc = rprint(f"[bold yellow]İndiriliyor: [white]{name}")
        self.current_progress = tqdm(
            desc=desc,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            miniters=1,
            total=0,
        )
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            if self.current_progress is not None:
                self.current_progress.close()
            
            return True
            
        except Exception as e:
            print(f"İndirme hatası: {str(e)}")
            if self.current_progress is not None:
                self.current_progress.set_description(f"❌ Hata: {name}")
                self.current_progress.close()
            return False
            
        finally:
            if self.current_progress is not None:
                self.current_progress.close()
            self.current_progress = None

    def _get_best_quality_url(self, episode_url):
        """En iyi kalite URL'sini al"""
        urls = self.api.fetch_anime_stream_api_url(episode_url)
        
        if not urls:
            return None
            
        # Kalite önceliği: 3 > 2 > 1 > 0
        for quality_index in [3, 2, 1, 0]:
            if quality_index < len(urls) and urls[quality_index].get('url'):
                return urls[quality_index]['url']
        
        return None

    def download_movie(self):
        if not self.anime_name or not self.anime_id:
            print("Anime bilgileri eksik!")
            return False
            
        anime_directory = self._create_directory(self.anime_name)
        download_url = self.api.fetch_anime_stream_api_url_movie(self.anime_id)
        file_path = os.path.join(anime_directory, f"{self.anime_name}.mp4")
        
        return self._download_video(download_url, file_path, self.anime_name)

    def download_episodes(self, selected_episodes=None):
        """Bölüm indirme"""
        if not self.episodes:
            print("Bölüm bilgileri bulunamadı!")
            return False
        
        if selected_episodes is None:
            episodes_to_download = self.episodes
        else:
            episodes_to_download = [
                episode for episode in self.episodes 
                if episode['name'] in selected_episodes
            ]

        if not episodes_to_download:
            print("İndirilecek bölüm bulunamadı.")
            return False

        anime_directory = self._create_directory(self.anime_name)
        success_count = 0
        
        print(f"Klasör: {anime_directory}")
        print(f"Toplam {len(episodes_to_download)} Bölüm İndirilecek\n")
        
        for i, episode in enumerate(episodes_to_download, 1):
            episode_name = episode['name']
            episode_url = episode['url']
            
            print(f"[{i}/{len(episodes_to_download)}] {episode_name}")
            
            download_url = self._get_best_quality_url(episode_url)
            if not download_url:
                print(f"URL bulunamadı: {episode_name}")
                continue
                
            file_path = os.path.join(anime_directory, f"{episode_name}.mp4")
            
            if self._download_video(download_url, file_path, episode_name):
                success_count += 1
                rprint(f"{episode_name} [bold green]Tamamlandı\n")
            else:
                rprint(f"{episode_name} [bold red]Başarısız\n")
            

        print(f"\n🎉 İndirme tamamlandı {success_count}/{len(episodes_to_download)} bölüm")
        clear()
        return success_count > 0

    def start_download(self, selected_episodes=None):
        """Ana indirme fonksiyonu"""
        if not self.anime_name or not self.anime_id:
            print("Anime bilgileri eksik!")
            return False
            
        print(f"İndirme başlatılıyor: {self.anime_name}")
    
        if self.episodes is None:
            return self.download_movie()
        else:
            return self.download_episodes(selected_episodes)