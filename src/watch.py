import requests
import subprocess
import time
import re


class WatchAnime:
    def __init__(self, use_vlc=False):
        self.base_url = "https://www.mangacix.net/"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        self.use_vlc = use_vlc

    def open_with_video_player(self,url):
        """Video Oynatıcı"""
        if self.use_vlc:
            try:
                if not isinstance(url, str):
                    raise ValueError("Url String Olmalı.")
                subprocess.run(['vlc', '-v', "--quiet", '--fullscreen', url], check=True)
            except subprocess.CalledProcessError as e:
                print("Oynatılırken Hata Oluştu!", e)
        else:
            try:
                subprocess.run(['mpv', '--fullscreen', url], check=True)
            except subprocess.CalledProcessError as e:
                print("Oynatılırken Hata Oluştu!", e)

    
