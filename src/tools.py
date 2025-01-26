# tools.py

import os, time
from InquirerPy import inquirer, prompt

def clear_screen():
    """Terminal Ekranını Temizle"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_website_selection_thing():
    """Website Seçim Penceresi"""
    clear_screen()
    choices= ["AnimeciX (ID: 856)", "Openani.me (ID: 525)"]
    l = [
        {
            "type":"list",
            "name":"website_selection",
            "message": "Bir Sağlayıcı Seçin.",
            "choices": choices,
            "border": True,
            "cycle":True,
        }
    ]
    l = prompt(l)
    selected_choices = l["website_selection"]
    print(selected_choices)
    return selected_choices

def display_website_selection_thing():
    """Website Seçim Penceresi"""
    clear_screen()
    choices= ["AnimeciX (ID: 856)", "Openani.me (ID: 525)"]
    l = [
        {
            "type":"list",
            "name":"website_selection",
            "message": "Bir Website Seçin.",
            "choices": choices,
            "border": True,
            "cycle":True,
        }
    ]
    l = prompt(l)
    selected_choices = l["website_selection"]
    print(selected_choices)
    return selected_choices

def play_current_episode(ani):
    """Şu anki Bölümü Oynat"""
    if ani.current_episode_index is not None:
        print(f"Bölüm Oynatılıyor: Bölüm, {ani.current_episode_index + 1}")  # Debug print
        ani.play_episode(ani.current_episode_index)
    else:
        print("Bölüm Seçilmedi!")
        time.sleep(0.8)

def next_episode(ani):
    """Siradaki Bölüme Git"""
    if ani.current_episode_index is not None and ani.current_episode_index < len(ani.episodes) - 1:
        ani.current_episode_index += 1
        #print(f"Next episode index: {ani.current_episode_index}")
    else:
        print("Sonraki Bölüm Yok!")
        time.sleep(0.8)

def previous_episode(ani):
    """Önceki Bölüme Git"""
    if ani.current_episode_index is not None and ani.current_episode_index > 0:
        ani.current_episode_index -= 1
        #print(f"Previous episode index: {ani.current_episode_index}")
    else:
        print("Önceki Bölüm Yok!")
        time.sleep(0.8)

def select_ep(ani):
    if ani.episodes:
        selected_name, _ = ani.select_episode(ani.episodes)
        ani.current_episode_index = next(
            (i for i, ep in enumerate(ani.episodes) if ep['name'] == selected_name), 
            None
        )
        if ani.current_episode_index is None:
            print("Seçilen Bölüm Bulunamadı!")
            time.sleep(0.8)
    else:
        print("Bölüm Bulunamadı!")
        time.sleep(0.8)
            
def invalid_option():
    """Geçersiz veri"""
    print("Geçersiz bir seçenek girdiniz. Lütfen geçerli bir seçenek giriniz.")
    time.sleep(1)

def exit_app():
    """Çık"""
    print("Çıkış yapılıyor...")
    time.sleep(0.6)
    exit()
