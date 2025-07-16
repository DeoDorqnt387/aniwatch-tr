import os
import yt_dlp
import re

from os import system, name
from prompt_toolkit import styles

from aniwatch_tr.core.config import get_download_folder
from pathlib import Path
from rich import print as rprint
from rich.panel import Panel
from rich.console import Group
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    SpinnerColumn,
    TimeElapsedColumn,
    DownloadColumn,
    TimeRemainingColumn,
    TaskProgressColumn,
    TransferSpeedColumn
)

prompt_style = styles.Style([
    ('qmark',        'fg:#707070 bold'),       # Tatlı sarı soru işareti
    ('question',     'fg:#707070 bold'),       # Beyazımsı açık soru metni
    ('answer',       'fg:#ffd166 bold'),       # Sıcak pastel sarı cevap
    ('pointer',      'fg:#ffe198 bold'),       # Aynı sarıdan ok
    ('highlighted',  'fg:#ffd166 bold'),       # Seçenek vurgusu
    ('selected',     'fg:#fefefe'),       # Seçili metin (arka plan yok)
    ('separator',    'fg:#aaaaaa'),            # Açık gri ayraç
    ('instruction',  'fg:#ffe198 italic'),     # Açıklama, sarı italic
    ('text',         'fg:#eeeeee'),            # Açık gri ana metin
    ('disabled',     'fg:#888888 italic'),     # Pasif itemler
])

def clear():
    system('cls' if name == 'nt' else 'clear')

def Status(message, hide=True, spinner="bouncingBar", color="black"):
    """    
    Args:
        message (str): Gösterilecek mesaj
        hide (bool): Bitince gizle
        spinner (str): Spinner tipi (ör. bouncingBar, dots, line, moon, earth, etc.)
        color (str): Yazı ve bar rengi
        
    Returns:
        Progress: Rich Progress instance
    """
    progress = Progress(
        SpinnerColumn(spinner),
        TextColumn(f"[red bold]{message}"),
        BarColumn(bar_width=40, style="black", pulse_style="bold red"),
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
        
        columns = (
            SpinnerColumn("bouncingBar"), 
            '[cyan]{task.description}',
            BarColumn(bar_width=40), 
            TaskProgressColumn(), 
            DownloadColumn(),
            TransferSpeedColumn(), 
            TimeRemainingColumn()
        )
        self.progress = Progress(*columns)
        self.current_task_id = None

    def setup_anime(self, anime_name, anime_id, episodes=None):
        self.anime_name = anime_name
        self.anime_id = anime_id
        self.episodes = episodes
        
    
    def _sanitize_filename(self, anime_name):
        return re.sub(r'[<>:"/\\|?*]', ' ', anime_name)
    
    def _create_directory(self, anime_name):
        custom_folder = get_download_folder()
        
        base_path = Path(custom_folder) if custom_folder else Path.home() / "Desktop"
        anime_directory = base_path / "Animeler" / self._sanitize_filename(anime_name)
        anime_directory.mkdir(parents=True, exist_ok=True)
        return str(anime_directory)

    def _progress_hook(self, d):
        status = d['status']
        
        if status == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_bytes = d.get('downloaded_bytes', 0)

            if self.current_task_id is None and total_bytes:
                self.current_task_id = self.progress.add_task(
                    "İndiriliyor...", 
                    total=total_bytes
                )
            
            if self.current_task_id is not None:
                if total_bytes:
                    self.progress.update(
                        self.current_task_id,
                        completed=downloaded_bytes,
                        total=total_bytes
                    )
                else:
                    downloaded_mb = downloaded_bytes / (1024 * 1024)
                    self.progress.update(
                        self.current_task_id,
                        description=f"İndiriliyor... {downloaded_mb:.1f} MB"
                    )
        
        elif status == 'finished':
            if self.current_task_id is not None:
                total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
                downloaded_bytes = d.get('downloaded_bytes', 0)
                
                final_size = downloaded_bytes or total_bytes
                if final_size:
                    self.progress.update(
                        self.current_task_id,
                        description="[green]İndirildi ✓",
                        completed=final_size,
                        total=final_size
                    )

                import time
                time.sleep(0.5)
                try:
                    self.progress.remove_task(self.current_task_id)
                except:
                    pass
                self.current_task_id = None
        
        elif status == 'error':
            if self.current_task_id is not None:
                self.progress.update(
                    self.current_task_id,
                    description="[red]❌ Hata"
                )

                import time
                time.sleep(1)
                try:
                    self.progress.remove_task(self.current_task_id)
                except:
                    pass
                self.current_task_id = None

    def _download_video(self, url, file_path, name):
        if not url:
            rprint(f"[red]Geçerli URL bulunamadı: {name}")
            return False

        ydl_opts = {
            'outtmpl': file_path,
            'progress_hooks': [self._progress_hook],
            'quiet': True,
            'no_warnings': True,
            'noprogress': True
        }
        
        self.current_task_id = None
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return True
            
        except Exception as e:
            rprint(f"[red]İndirme hatası: {str(e)}")
            if self.current_task_id is not None:
                self.progress.update(
                    self.current_task_id,
                    description=f"[red]❌ Hata: {name}"
                )
                try:
                    self.progress.remove_task(self.current_task_id)
                except:
                    pass
                self.current_task_id = None
            return False

    def _get_best_quality_url(self, episode_url):
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
            rprint("[red]Anime bilgileri eksik!")
            return False
            
        anime_directory = self._create_directory(self.anime_name)
        download_url = self.api.fetch_anime_stream_api_url_movie(self.anime_id)
        file_path = os.path.join(anime_directory, f"{self.anime_name}.mp4")
        
        with self.progress:
            return self._download_video(download_url, file_path, self.anime_name)

    def download_episodes(self, selected_episodes=None):
        if not self.episodes:
            rprint("[red]Bölüm bilgileri bulunamadı!")
            return False
        
        if selected_episodes is None:
            episodes_to_download = self.episodes
        else:
            episodes_to_download = [
                episode for episode in self.episodes 
                if episode['name'] in selected_episodes
            ]

        if not episodes_to_download:
            rprint("[red]İndirilecek bölüm bulunamadı.")
            return False

        anime_directory = self._create_directory(self.anime_name)
        success_count = 0
        
        rprint(f"[cyan]Klasör: [white]{anime_directory}")
        rprint(f"[cyan]Toplam [white]{len(episodes_to_download)} Bölüm İndirilecek\n")
        
        with self.progress:
            for i, episode in enumerate(episodes_to_download, 1):
                episode_name = episode['name']
                episode_url = episode['url']
                
                rprint(f"[cyan][{i}/{len(episodes_to_download)}] [white]{episode_name}")
                
                download_url = self._get_best_quality_url(episode_url)
                if not download_url:
                    rprint(f"[red]URL bulunamadı: {episode_name}")
                    continue
                    
                file_path = os.path.join(anime_directory, f"{episode_name}.mp4")
                
                if self._download_video(download_url, file_path, episode_name):
                    success_count += 1
                    rprint(f"[green]✓ {episode_name} Tamamlandı\n")
                else:
                    rprint(f"[red]✗ {episode_name} Başarısız\n")

        rprint(f"\n🎉 İndirme tamamlandı {success_count}/{len(episodes_to_download)} bölüm")
        clear()
        return success_count > 0
    
    def start_download(self, selected_episodes=None):
        if not self.anime_name or not self.anime_id:
            rprint("[red]Anime bilgileri eksik!")
            return False
            
        rprint(f"[cyan]İndirme başlatılıyor: [white]{self.anime_name}")
    
        if self.episodes is None:
            return self.download_movie()
        else:
            return self.download_episodes(selected_episodes)
