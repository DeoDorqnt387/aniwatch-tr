import subprocess
import os
import urllib.parse

from aniwatch_tr.core.config import load_config, get_fullscreen

config = load_config()

class MediaPlayer:
    def __init__(self):
        self.players = {
            'mpv': {'cmd': 'mpv', 'name': 'MPV Player'},
            'vlc': {'cmd': 'vlc', 'name': 'VLC Media Player'}
        }
        self.common_paths = {
            'mpv': [
                r"C:\Program Files\mpv\mpv.exe",
                r"C:\Program Files (x86)\mpv\mpv.exe"
            ],
            'vlc': [
                r"C:\Program Files\VideoLAN\VLC\vlc.exe",
                r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"
            ]
        }
    
    def find_available_players(self):
        available = []
        
        for player_id, player_info in self.players.items():
            if self.is_player_available(player_id):
                available.append((player_id, player_info['name']))
        
        return available
    
    def is_player_available(self, player_id):
        if player_id not in self.players:
            return False
            
        player_info = self.players[player_id]
        
        # PATH'te kontrol et
        try:
            subprocess.run([player_info['cmd'], '--version'], 
                         capture_output=True, timeout=5)
            return True
        except:
            pass
        
        # Yaygın yollarda kontrol et
        if player_id in self.common_paths:
            for path in self.common_paths[player_id]:
                if os.path.exists(path):
                    self.players[player_id]['cmd'] = path
                    return True
        
        return False
    
    def play(self, url, player='mpv', subtitle_url=None):
        """Belirtilen oynatıcı ile medya dosyasını oynatır"""
        if player not in self.players:
            raise ValueError(f"Desteklenmeyen oynatıcı: {player}. Desteklenenler: {', '.join(self.players.keys())}")
        
        if not self.is_player_available(player):
            raise RuntimeError(f"Oynatıcı bulunamadı: {self.players[player]['name']}")
        
        player_info = self.players[player]
        fullscreen = get_fullscreen()
        
        try:
            args = [player_info['cmd'], url]
            
            if subtitle_url:
                if player == 'mpv':
                    args.append(f'--sub-file={subtitle_url}')
                elif player == 'vlc':
                    args.extend(['--input-slave', subtitle_url])
                
                    #print(f"Using subtitle: {clean_url}")
                    #print(f"Original subtitle URL: {subtitle_url}")
                    #print(f"Processed subtitle URL: {clean_url}")
            
            if fullscreen:
                if player == 'mpv':
                    args.append('--fullscreen')
                elif player == 'vlc':
                    args.append('--fullscreen')

            subprocess.Popen(args)
            
            #print(f"Medya {player_info['name']} ile oynatılıyor...")
            
        except subprocess.CalledProcessError as e:
            print(f"Oynatma hatası: {e}")
        except Exception as e:
            print(f"Beklenmeyen hata: {e}")
    
    def list_players(self):
        """Mevcut oynatıcıları listeler"""
        available = self.find_available_players()
        
        print("Mevcut medya oynatıcıları:")
        for player_id, player_name in available:
            status = "✓" if self.is_player_available(player_id) else "✗"
            print(f"  {status} {player_id}: {player_name}")
        
        return available

def play(url, player, subtitle_url=None):
    media_player = MediaPlayer()
    media_player.play(url, player, subtitle_url)
