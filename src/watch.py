import subprocess

def open_with_video_player(url):
    """Video Oynatıcı"""
    try:
        subprocess.run(['mpv', '--fullscreen', url], check=True)
    except subprocess.CalledProcessError as e:
        print("Oynatılırken Hata Oluştu!", e)
