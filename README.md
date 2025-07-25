<h1 align="center">
Aniwatch-TR
</h1>

<h3 align="center">
    <img src="https://img.shields.io/badge/Animecix.net - Çalışıyor-green?style=for-the-badge">
    <img src="https://img.shields.io/badge/Openani.me - Devre dışı-red?style=for-the-badge">
</h3>

<h3 align="center">
    Terminalden Türkçe anime izleme, indirme.
</h3>

[demo.webm](https://github.com/user-attachments/assets/f71ebc74-edb6-4aeb-baaa-72fc4fd4daf1)

---

## 📑 İçindekiler
- [Bilinen Sorunlar](#bilinen-sorunlar)
- [Gereksinimler](#gereksinimler)
    - [Linux](#linux)
    - [Windows](#windows)
- [Config Dosyası](#config-dosyası)
- [Kurulum](#-kurulum)
    - [PIP ile Kurulum](#-pip-ile-kurulum)
    - [Windows için .exe Dosyası](#-windows-için-exe-dosyası)
- [Kullanım](#-kullanım)
- [Nasıl Kaldırılır?](#-nasıl-kaldırılır)

---
## Bilinen Sorunlar
- Movie(film) izleyememe sorunu.
  
<sub>Bunlar bildiğim ve yakın zamanda çözmeyi planladığım şeyler.</sub>

---

## Gereksinimler

## Linux

### MPV / VLC / Tkinter

Linux (Arch/Arch-tabanlı)
```bash
sudo pacman -S mpv vlc python3-tk
```

## Windows

### Python
Aniwatch-TR’yi kullanabilmek için bilgisayarınızda **Python 3.9 ile 3.12** sürümleri arasında bir sürüm kurulu olmalıdır.  
Python 3.13 ve üzerinde test etmedim, çalışmayabilir. [Python resmi sitesi](https://www.python.org/downloads/)

### MPV/VLC

Kurulum için resmi siteleri ziyaret edebilirsiniz: - [MPV](https://mpv.io/)  - [VLC](https://www.videolan.org/vlc/)

---

### Config Dosyası
Config Dosyası Programı ilk açtığınızda oluşan, yaptığınız ayarların depolandığı yerdir ve Şöyle gözükmektedir:

```bash
{
    "player": "mpv", # Mpv / Vlc Seçimi
    "provider": "Animecix.tv", # Sağlayıcılar
    "video_quality": "En Yüksek Kalite", ## En Düşük ve En yüksek kalite
    "fullscreen": true, ## Tam Ekran Aç/Kapa
    "download_folder": "C:\\Users\\<kullanici-adiniz>\\.aniwatch-tr\\downloads" # Varsayılan/Değiştirilmemiş
}
```
Herhangi bir ayarı değiştirdiğinizde config.json dosyası değişmektedir.

Windows'da Config.json dosyası şurada yer almaktadır:
```bash
C:\Kullanıcılar\<kullanıcı-adınız>\.aniwatch-tr\config.json
```
Linux'da ise şurada:
```bash
/home/<kullanıcı-adınız>/.aniwatch-tr/config.json
```
Herhangi bir sorun yaşarsanız config.json'u el ile düzeltebilirsiniz.

---

## 💻 Kurulum

## 📦 PIP ile Kurulum

Aniwatch-TR’yi pip ile kolayca kurabilirsiniz(Windows/Linux):

```bash
pip install aniwatch-tr
```

---

## 🪟 Windows için .exe Dosyası
Windows kullanıyorsanız, hiçbir bağımlılıkla uğraşmadan çalıştırmak için aşağıdaki linkten .exe dosyasını indirebilirsiniz:

👉 [Aniwatch-TR Releases](https://github.com/DeoDorqnt387/aniwatch-tr/releases)

<img width="167" height="121" alt="image" src="https://github.com/user-attachments/assets/1b26525e-f6de-4906-a9e0-4c3bb9709d21" />

> [!WARNING]  
> Sertifikası olmadığından dolayı windows dosyayı virus olarak algılıyor, aklınızda bulunsun.

## 🚀 Kullanım
Kurulum sonrası terminal veya komut istemcisine şunu yazmanız yeterli:
```bash
aniwatch-tr
```

## ❌ Nasıl Kaldırılır?
Kurulumu kaldırmak için:
```bash
pip uninstall aniwatch-tr
```
Windows için .exe kullanıyorsanız, dosyayı silmeniz yeterlidir.
> [!WARNING]  
> <sub>Config dosyasını da silmeyi unutmayın.</sub>

---

[ani-cli](https://github.com/pystardust/ani-cli)'den Esinlenilmiştir.
