import subprocess

def open_with_video_player(url, use_vlc=False):
    """Video Oynatıcı"""
    if use_vlc:
        try:
            if not isinstance(url, str):
                raise ValueError("Url must be a string.")
            subprocess.run(['vlc', '-v', "--quiet", '--fullscreen', url], check=True)
        except subprocess.CalledProcessError as e:
            print("Oynatılırken Hata Oluştu!", e)
    else:
        try:
            subprocess.run(['mpv', '--fullscreen', url], check=True)
        except subprocess.CalledProcessError as e:
            print("Oynatılırken Hata Oluştu!", e)


