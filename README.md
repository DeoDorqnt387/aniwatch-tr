<h1 align="center">
<strong> AniWatch-tr </strong>
</h1>

<h3 align="center">
    <img src="https://img.shields.io/badge/Animecix.net - Çalışıyor-green?style=for-the-badge">
    <img src="https://img.shields.io/badge/Openani.me - Çalışıyor-green?style=for-the-badge">
</h3>

<h3 align="center">
    Terminalden Türkçe anime izleme, indirme.
</h3>

[![Video Thumbnail](https://github.com/user-attachments/assets/311a0f45-91f9-44dc-827a-47a623876d86)](https://github.com/user-attachments/assets/311a0f45-91f9-44dc-827a-47a623876d86)

## ![Ode to Joy](https://github.com/user-attachments/assets/10ab0055-4c5b-4530-9eb9-1b86ed572425) ÖN GEREKSİNİMLER

Bilgisayarınızda [**mpv**](https://github.com/mpv-player/mpv) programının kurulu olduğundan emin olun. Eğer kurulu değilse, aşağıdaki adımları izleyerek kurabilirsiniz:

**Arch/Arch-Based:**
```bash
sudo pacman -S mpv yt-dlp
```
**Ubuntu/Debian**
```bash
sudo apt-get install mpv yt-dlp
```
**Fedora**
```bash
sudo dnf install mpv yt-dlp
```
**OpenSUSE**
```bash
sudo zypper install mpv yt-dlp
```
---

**Windows**
 [Scoop ile kurulum](https://adamtheautomator.com/scoop-windows/):
```bash
scoop install mpv
```
**Windows Manual Kurulum**:

[MPV](https://github.com/shinchiro/mpv-winbuild-cmake/releases) Uygulamasını Path'e ekleyin.


## ![Eine kleine Nachtmusik](https://github.com/user-attachments/assets/7680f19d-66c1-4c82-b962-93b6f6e24a0a) KURULUM

**PIP**
```bash
pip install aniwatch-tr #Bozuk Çalışmıyor, Windows'a zip olarak indirip çalıştırmayı deneyin.
```

**Manual Kurulum**
```bash
cd ~ && git clone https://github.com/DeoDorqnt387/aniwatch-tr.git && bash aniwatch-tr/install.sh
```
```bash
sudo cp ~/.aniwatch-tr/aniwatch-tr /usr/local/bin/aniwatch-tr
```

## ![Fantaisie Impromptu](https://github.com/user-attachments/assets/ca9a7912-d73c-4982-aa87-742fd3b75264) KULLANIM


```bash
aniwatch-tr
```

## ![Pomp and Circumstance](https://github.com/user-attachments/assets/224c3e08-3aa1-4cf6-9a36-9c8e63c21638) NASIL KALDIRILIR?


```bash
sudo rm /usr/local/bin/aniwatch-tr && sudo rm -rf ~/.aniwatch-tr
```

<hr>

[Ani-cli](https://github.com/pystardust/ani-cli)'den Esinlenilmiştir.
