"""Aniwatch-TR"""
import questionary
import time

from rich import print as rprint
from rich.table import Table
from rich.live import Live
from aniwatch_tr.cli.tools_cli import prompt_style,clear,Status,Download
from aniwatch_tr.core.player import play
from aniwatch_tr.api.animeci import AnimeciAPI
from aniwatch_tr.version import aniwatch_status, current_version
from aniwatch_tr.core.config import (
    save_config, 
    load_config, 
    set_provider,
    set_download_folder, 
    set_player,
    set_video_quality,
    set_fullscreen,
    get_video_quality,
    get_download_folder,
    get_player,
    get_fullscreen,
    get_provider
)

#print(config)
#time.sleep(5)

def check_pip_status():
    with Status("Güncellemeler kontrol ediliyor.."):
        clear()
        time.sleep(1.5)
    print(f"📦 Versiyon: {current_version()}")
    print(" ")
    print(aniwatch_status())
    print(" ")
    print("✅ Program hazır!\n")

def menu(ani):
    downloader = None

    while True:
        clear()
        select_is1 = questionary.select(
            "Seçenek Seçin:",
            choices=[
                "Anime izle",
                "Ayarlar",
                "Çık"
            ],
            style=prompt_style,
            instruction=" "
        ).ask()
        if not select_is1:
            break

        if "Anime izle" in select_is1:
            try:
                
                query = questionary.text(
                    "Anime Ara:",
                    style=prompt_style
                ).ask()

                with Status("Anime Aranıyor.."):
                    time.sleep(0.7)
                clear()
                search_data = ani.fetch_anime_search_data(query)
                anime_dict = {
                    item["name"]: item.get("id")
                    for item in search_data
                }

                if not list(anime_dict.keys()):
                    rprint("[red]Hiçbir sonuç bulunamadı.[/red]")
                    time.sleep(1.5)
                    continue
                
                q = questionary.select(
                    f"Bir anime Seçin:",
                    choices=list(anime_dict.keys()),
                    style=prompt_style,
                    instruction=" "          
                ).ask()
                clear()
                #print("seçilen anime: ",q)

                anime_name = q
                anime_id = anime_dict.get(q)
                ## print(selected_id)
                time.sleep(0.05)
            except (KeyError, IndexError):
                rprint("[red][strong]Anime bulunamadı.[/strong][/red]")
                time.sleep(1.5)
                continue

            selected_index = 0
            episode_name = ""

            while True:
                with Status("Veriler Toplanıyor.."):
                    seasons = ani.fetch_anime_seasons(anime_id)
                    episodes = ani.fetch_anime_episodes(anime_id)

                ## print(str(seasons))
                ## print(str(episodes))

                if not episodes or not seasons:
                    rprint("[red]Hiç bölüm bulunamadı.[/red]")
                    time.sleep(1.5)
                    break
                
                if episode_name == "":
                    episode_name = episodes[selected_index]["name"]
                
                select_is2 = questionary.select(
                    "Seçenek Seçin",
                    choices=[
                        f"Bölüm İzle: {episode_name}",
                        "Sonraki Bölüm",
                        "Önceki Bölüm",
                        "Bölüm Seç",
                        "Bölüm indir",
                        "Geri"
                    ],
                    style=prompt_style,
                    instruction=" "
                ).ask()

                if "Bölüm İzle" in select_is2:
                    with Status("Bölüm Hazırlanıyor.."):
                        stream = ani.fetch_anime_stream_api_url(episodes[selected_index]["url"])
                    #print(stream)
                    video_quality = get_video_quality()
                    selected_stream = stream[-1] if video_quality == "En Düşük Kalite" else stream[0]

                    #print(f"Seasons type: {type(seasons)}")
                    #print(f"Seasons value: {seasons}")
                    
                    try:
                        if isinstance(seasons, list) and len(seasons) > 0:
                            season_index = seasons[0]["index"]
                        else:
                            season_index = seasons if isinstance(seasons, int) else 1
                    except (TypeError, KeyError, IndexError):
                        season_index = 1


                    captions = ani.fetch_captions_for_the_humanity(season_index, selected_index, anime_id)
                    if captions:
                        selected_stream["captions"] = captions
                        #print(f"Caption URL: {selected_stream['captions']}")
                    else:
                        pass
                        #rprint("[yellow]Caption bulunamadı")

                    # print(selected_stream["url"])
                    play(selected_stream["url"], get_player(), captions)
                    clear()
                    
                elif "Bölüm Seç" in select_is2:
                    with Status("Bölümler Getiriliyor.."):
                        time.sleep(0.7)
                    episode = questionary.select(
                        "Bölüm Seçin:",
                        choices=[ep["name"] for ep in episodes],
                        style=prompt_style,
                        instruction=" "
                    ).ask()

                    episode_name = episode

                    selected_index = next(
                        (i for i, ep in enumerate(episodes) if ep["name"] == episode_name), 0)
                    clear()
                    
                elif "Sonraki" in select_is2:
                    if selected_index < len(episodes) - 1:
                        selected_index += 1
                        episode_name = episodes[selected_index]["name"]
                        clear()
                    else:
                        rprint("[yellow]Son bölümdesin.[/yellow]")

                elif "Önceki" in select_is2:
                    if selected_index > 0:
                        selected_index -= 1
                        episode_name = episodes[selected_index]["name"]
                        clear()
                    else:
                        rprint("[yellow]İlk bölümdesin.[/yellow]")

                elif "Bölüm indir" in select_is2:
                    with Status("Biraz Bekleyin.."):
                        time.sleep(0.7)
                    downloader = Download(ani)
                    select_is3 = questionary.select(
                        "Seçenek Seçin",
                        choices=[
                            "Tüm Bölümleri İndir",
                            "Bölüm Seç",
                            "Geri",
                        ],
                        style=prompt_style,
                        instruction=" "
                    ).ask()
                    
                    if "Tüm Bölümleri İndir" in select_is3:
                        # Tüm bölümleri indir
                        downloader.setup_anime(anime_name, anime_id, episodes)
                        downloader.start_download()  # selected_episodes=None (tümü)
                        clear()
                        
                    elif "Bölüm Seç" in select_is3:
                        # Bölüm seçimi yap ve indir
                        if episodes:
                            episode_names = [ep['name'] for ep in episodes]
                            selected_episodes = questionary.checkbox(
                                "İndirmek istediğiniz bölümleri seçin:",
                                choices=episode_names,
                                style=prompt_style,
                                instruction="Hareket etmek için ok tuşlarını kullanın. <space> ile seç, <enter> ile onayla."
                            ).ask()
                            
                            if selected_episodes:
                                downloader.setup_anime(anime_name, anime_id, episodes)
                                downloader.start_download(selected_episodes)
                            else:
                                rprint("[yellow]Hiçbir bölüm seçilmedi.[/yellow]")
                        else:
                            rprint("[red]Bölüm bilgileri bulunamadı![/red]")
                    elif "Geri" in select_is3:
                        break
                elif "Geri" in select_is2:
                    break

        elif "Ayarlar" in select_is1:
            clear()
            while True:
                select_is5 = questionary.select(
                    "Seçenek Seçin",
                    choices=[
                        f"Oynatıcı Seçimi: {get_player()}",
                        f"Oynatıcı Tam Ekran Aç/Kapa: {get_fullscreen()}",
                        f"Sağlayıcı Seçimi: {get_provider()}",
                        f"Bölüm İndirme Klasörünü Seç: {get_download_folder()}",
                        f"Video Kalitesi Seçin: {get_video_quality()}",
                        "Geri"
                    ],
                    style=prompt_style,
                    instruction=" "
                ).ask()

                if "Oynatıcı Seçimi" in select_is5:
                    new_player = questionary.select(
                        "Oynatıcı Seçin",
                        choices=["mpv", "vlc"],
                        style=prompt_style
                    ).ask()
                    set_player(new_player)
                    clear()

                elif "Oynatıcı Tam" in select_is5:
                    new_fs = questionary.select(
                        "Tam ekran modunu seçin:",
                        choices=["True", "False"],
                        style=prompt_style
                    ).ask()
                    set_fullscreen(new_fs)
                    clear()

                elif "Sağlayıcı Seçimi" in select_is5:
                    new_provider = questionary.select(
                        "Seçenek Seçin",
                        choices=["Animecix.tv"],
                        style=prompt_style,
                        instruction=" "
                    ).ask()
                    set_provider(new_provider)
                    clear()

                elif "Video" in select_is5:
                    new_quality = questionary.select(
                        "Video Kalitesi Seçin:",
                        choices=[
                            "En Yüksek Kalite",
                            "En Düşük Kalite"
                        ],
                        style=prompt_style,
                        instruction=" "
                    ).ask()
                    set_video_quality(new_quality)
                    clear()

                elif "Bölüm İndirme Klasör" in select_is5:
                    import tkinter as tk
                    from tkinter import filedialog

                    tk.Tk().withdraw()
                    download_folder = filedialog.askdirectory(title="Klasör Seç")
                    if download_folder:
                        set_download_folder(download_folder)
                        print(f"Yeni klasör: {download_folder}")
                        clear()

                elif select_is5 == "Geri":
                    break

        elif "Çık" in select_is1:
            with Status("Programdan Çıkılıyor.."):
                clear()
                time.sleep(0.7)
            break
        
def main():
    ## Check for updates
    check_pip_status()

    time.sleep(2.5)

    provider = get_provider()
    if provider == "Animecix.tv":
        ani = AnimeciAPI()
    else:
        raise Exception("Desteklenmeyen provider! Config Dosyanızı Kontrol Edin!")
    
    menu(ani)

if __name__ == "__main__":
    main()
