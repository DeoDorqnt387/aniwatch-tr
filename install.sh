#!/bin/bash

# İzinleri ayarlama ve dosyayı taşımak
sudo chmod +x aniwatch-tr
sudo mv aniwatch-tr /usr/local/bin

# Kaynak dizinini taşımak ve izinlerini ayarlamak
sudo cp ~/aniwatch-tr/main.py /usr/local/bin/aniwatch-tr
sudo chmod +x /usr/local/bin/aniwatch-tr
export PYTHONPATH=$PYTHONPATH:~/aniwatch-tr
# Sanal ortamı oluşturup gerekli paketleri yüklemek
cd ~/.aniwatch-tr_src

# Python sanal ortamını oluşturma
python3 -m venv .venv

# Paketleri yükleme
.venv/bin/pip install -r requirements.txt
