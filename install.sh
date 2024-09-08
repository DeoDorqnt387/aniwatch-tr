#!/bin/bash

# İzinleri ayarlama ve dosyayı taşımak
sudo chmod +x aniwatch-tr
sudo mv aniwatch-tr /usr/local/bin/

# Kaynak dizinini taşımak ve izinlerini ayarlamak
if [ -f ~/aniwatch-tr/main.py ]; then
  sudo cp ~/aniwatch-tr/main.py /usr/local/bin/aniwatch-tr
  sudo chmod +x /usr/local/bin/aniwatch-tr
else
  echo "Dosya bulunamadı: ~/aniwatch-tr/main.py"
  exit 1
fi

# PYTHONPATH ayarlamak
export PYTHONPATH=$PYTHONPATH:~/aniwatch-tr

# Sanal ortamı oluşturup gerekli paketleri yüklemek
cd ~/.aniwatch-tr_src || { echo "Dizin mevcut değil: ~/.aniwatch-tr_src"; exit 1; }

# Python sanal ortamını oluşturma
python3 -m venv .venv

# Paketleri yükleme
.venv/bin/pip install -r requirements.txt
