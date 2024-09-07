#!/bin/bash

# Proje dizinine geç
cd "$(dirname "$0")"

# Program dosyasını çalıştırılabilir yap
chmod +x main.py

# Programı /usr/local/bin dizinine taşı ve PATH'e ekle
sudo ln -sf "$(pwd)/main.py" /usr/local/bin/aniwatch-tr

# Python sanal ortamını oluştur ve bağımlılıkları yükle
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

echo "Kurulum tamamlandı. 'aniwatch-tr' komutunu kullanarak programı çalıştırabilirsiniz."
