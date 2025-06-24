import subprocess, time

def open_with_video_player(url):
    """Video Oynatıcı"""
    if not url:
        print("TER: Video Url'si boş...")
        time.sleep(3)

    print("Video Çıkarılıyor...")

    # Tek sorunu animecix'e de bunu vermesi, ama çalıştığı için ellemeyeceğim sıkıntı  yok.
    mpv_args = [
        'mpv',
        '--fullscreen',
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        '--referrer=https://openani.me',
        '--http-header-fields=Origin: https://openani.me',
        '--no-ytdl',  # yt-dlp kullanmayı devre dışı bırak
        url
    ]
    
    try:
        subprocess.run(mpv_args, check=True)
    except subprocess.CalledProcessError as e:
        print("Oynatılırken Hata Oluştu!", e)
        time.sleep(10)
