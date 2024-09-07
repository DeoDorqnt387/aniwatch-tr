#!/bin/bash

# Proje dizinine geç
cd "$(dirname "$0")"

# Python sanal ortamını oluştur
python3 -m venv .venv
source .venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Python dosyasına çalıştırma izni ver
chmod +x main.py
# Betiğe çalıştırma izni ver
sudo chmod +x /usr/local/bin/aniwatch-tr

echo "Kurulum tamamlandı. 'aniwatch-tr' komutunu kullanarak programı çalıştırabilirsiniz."
