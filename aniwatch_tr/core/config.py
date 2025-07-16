import os
import json

# Kullanıcı dizini altında config yolu
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".aniwatch-tr")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

# Varsayılan config içeriği
DEFAULT_CONFIG = {
    "player": "mpv", # MPV/VLC
    "provider": "Animecix.tv", # Sağlayıcı
    "video_quality": "En Yüksek Kalite", # En Düşük ve En yüksek kalite
    "fullscreen": True, # Tam Ekran Aç/Kapa
    "download_folder": os.path.join(CONFIG_DIR, "downloads") # Klasör Yolu
}


def ensure_config_exists():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    if not os.path.exists(CONFIG_PATH):
        # Dosya Yoksa Yarat
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4, ensure_ascii=False)


def load_config():
    ensure_config_exists()
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(data):
    ensure_config_exists()
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


## SET ##
def set_player(player):
    config = load_config()
    config["player"] = player
    save_config(config)


def set_provider(provider):
    config = load_config()
    config["provider"] = provider
    save_config(config)


def set_download_folder(path):
    config = load_config()
    config["download_folder"] = path
    save_config(config)


def set_video_quality(quality):
    config = load_config()
    config["video_quality"] = quality
    save_config(config)


def set_fullscreen(is_fullscreen):
    config = load_config()
    config["fullscreen"] = is_fullscreen
    save_config(config)

## GET ##
def get_download_folder():
    config = load_config()
    return config.get("download_folder", "")

def get_player():
    config = load_config()
    return config.get("player", "mpv")

def get_provider():
    config = load_config()
    return config.get("provider", "Animecix.tv")

def get_video_quality():
    config = load_config()
    return config.get("video_quality", "En Yüksek Kalite")

def get_fullscreen():
    config = load_config()
    return config.get("fullscreen", False)
