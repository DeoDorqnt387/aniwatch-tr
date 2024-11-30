<h1 align="center">
<strong> AniWatch-tr </strong>
</h1>

<h4 align="center">
TÜRKÇE | <a href="https://github.com/DeoDorqnt387/aniwatch-tr/blob/main/eng.md">ENGLISH</a>
</h4>

<h3 align="center">
    Terminalden Türkçe anime izleme, indirme.
</h3>

[![Video Thumbnail](https://github.com/user-attachments/assets/311a0f45-91f9-44dc-827a-47a623876d86)](https://github.com/user-attachments/assets/311a0f45-91f9-44dc-827a-47a623876d86)

<h1 align="center">
    <b>Ön Gereksinim</b>
</h1>

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
<hr>

**Windows**
 [Scoop ile kurulum](https://adamtheautomator.com/scoop-windows/):
```bash
scoop install mpv
```
**Windows Manual Kurulum**:

[MPV](https://github.com/shinchiro/mpv-winbuild-cmake/releases) Uygulamasını Path'e ekleyin.

<h1 align="center">
    <b>Kurulum</b>
</h1>

**PIP**
```bash
pip install aniwatch-tr #v0.3.8
```

**Manual Kurulum**
```bash
cd ~ && git clone https://github.com/DeoDorqnt387/aniwatch-tr.git && bash aniwatch-tr/install.sh
```
```bash
sudo cp ~/.aniwatch-tr/aniwatch-tr /usr/local/bin/aniwatch-tr
```
**Kullanım**
```bash
aniwatch-tr
```
```bash
aniwatch-tr -v # Opsyionel VLC Kullanımı
```
```bash
aniwatch-tr -r (480p, 720p, 1080p) # Çözünürlük Seçimi Opsiyonel (Varsayılan En Yüksek Çözünürlük)
```
**Nasıl Kaldırılır?**
```bash
sudo rm /usr/local/bin/aniwatch-tr && sudo rm -rf ~/.aniwatch-tr
```

<hr>

[Ani-cli](https://github.com/pystardust/ani-cli)'den Esinlenilmiştir.
