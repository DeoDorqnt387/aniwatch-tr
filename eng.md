<h1 align="center">
<strong> AniWatch-tr </strong>
</h1>

<h4 align="center">
english | <a href="https://github.com/DeoDorqnt387/aniwatch-tr">türkçe</a>
</h4>

<h3 align="center">
Stream and Download Turkish Anime From the Terminal.
</h3>

[![Video Thumbnail](https://github.com/user-attachments/assets/44b9d628-f96c-4baf-aec1-28e9f2472621)](https://github.com/user-attachments/assets/44b9d628-f96c-4baf-aec1-28e9f2472621)

<h1 align="center">
    <b>Prerequisite</b>
</h1>

Make sure you have the [**mpv**](https://github.com/mpv-player/mpv) program installed on your computer. If not, you can install it by following the steps below:

**Arch:**
```bash
sudo pacman -S mpv
```
**Ubuntu/Debian**
```bash
sudo apt-get install mpv
```
**Fedora**
```bash
sudo dnf install mpv
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
aniwatch-tr -v # Opsyionel VLC Kullanımı
```
**How to Remove??**
```bash
sudo rm /usr/local/bin/aniwatch-tr && sudo rm -rf ~/.aniwatch-tr
```
<hr>

Inspired by [Ani-cli](https://github.com/pystardust/ani-cli)'
