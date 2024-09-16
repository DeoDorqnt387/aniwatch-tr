<h1 align="center">
<strong> AniWatch-tr </strong>
</h1>

<h4 align="center">
ENGLISH | <a href="https://github.com/DeoDorqnt387/aniwatch-tr">TÜRKÇE</a>
</h4>

<h3 align="center">
Stream and Download Turkish Anime From the Terminal.
</h3>

[![Video Thumbnail](https://github.com/user-attachments/assets/311a0f45-91f9-44dc-827a-47a623876d86)](https://github.com/user-attachments/assets/311a0f45-91f9-44dc-827a-47a623876d86)

<h1 align="center">
    <b>Prerequisite</b>
</h1>

Make sure you have the [**mpv**](https://github.com/mpv-player/mpv) program installed on your computer. If not, you can install it by following the steps below:

**Arch:**
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

> [!WARNING]
> In Windows, you need to add the [MPV](https://github.com/shinchiro/mpv-winbuild-cmake/releases) application to Path.

<h1 align="center">
    <b>Installation</b>
</h1>

**PIP**
```bash
pip install aniwatch-tr
```

**Manual Installation**
```bash
cd ~ && git clone https://github.com/DeoDorqnt387/aniwatch-tr.git && bash aniwatch-tr/install.sh
```
```bash
sudo cp ~/.aniwatch-tr/aniwatch-tr /usr/local/bin/aniwatch-tr
```
**Usage**
```bash
aniwatch-tr
```
```bash
aniwatch-tr -v # Optional Vlc Usage
```
```bash
aniwatch-tr -r (480p, 720p, 1080p) # Resolution Selection Optional (Default Highest Resolution)
```
**How to Remove??**
```bash
sudo rm /usr/local/bin/aniwatch-tr && sudo rm -rf ~/.aniwatch-tr
```
<hr>

Inspired by [Ani-cli](https://github.com/pystardust/ani-cli)'
