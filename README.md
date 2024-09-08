<h1 align="center">
<strong> AniWatch-tr </strong>
</h1>

<h3 align="center">
    Terminalden anime izleme, indirme.
</h3>

[![Video Thumbnail](https://github.com/user-attachments/assets/514c2fbb-2f04-4bac-84c3-32c4d563caa3)](https://github.com/user-attachments/assets/514c2fbb-2f04-4bac-84c3-32c4d563caa3)

<h1 align="center">
    <b>Ön Gereksinim</b>
</h1>

Bilgisayarınızda **mpv** programının kurulu olduğundan emin olun. Eğer kurulu değilse, aşağıdaki adımları izleyerek kurabilirsiniz:

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
<h1 align="center">
    <b>Kurulum</b>
</h1>

```bash
cd ~ && git clone https://github.com/DeoDorqnt387/aniwatch-tr.git && bash aniwatch-tr/install.sh
sudo cp ~/aniwatch-tr/main.py /usr/local/bin/aniwatch-tr
sudo chmod +x /usr/local/bin/aniwatch-tr
export PYTHONPATH=$PYTHONPATH:~/aniwatch-tr
```
**Nasıl Kaldırılır?**
```bash
sudo rm -r /usr/local/bin/aniwatch-tr
```
