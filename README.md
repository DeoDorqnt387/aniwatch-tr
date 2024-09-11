<h1 align="center">
<strong> AniWatch-tr </strong>
</h1>

<h3 align="center">
    Terminalden Türkçe anime izleme, indirme.
</h3>

[![Video Thumbnail](https://github.com/user-attachments/assets/44b9d628-f96c-4baf-aec1-28e9f2472621)](https://github.com/user-attachments/assets/44b9d628-f96c-4baf-aec1-28e9f2472621)

<h1 align="center">
    <b>Ön Gereksinim</b>
</h1>

Bilgisayarınızda [**mpv**](https://github.com/mpv-player/mpv) programının kurulu olduğundan emin olun. Eğer kurulu değilse, aşağıdaki adımları izleyerek kurabilirsiniz:

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
> Windows'ta [MPV](https://github.com/shinchiro/mpv-winbuild-cmake/releases) uygulamasını Path'e Eklemeniz Gerekmekte.

<h1 align="center">
    <b>Kurulum</b>
</h1>

**PIP**
```bash
pip install aniwatch-tr
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
**Nasıl Kaldırılır?**
```bash
sudo rm /usr/local/bin/aniwatch-tr && sudo rm -rf ~/.aniwatch-tr
```

<hr>

[Ani-cli](https://github.com/pystardust/ani-cli)'den Esinlenilmiştir.
