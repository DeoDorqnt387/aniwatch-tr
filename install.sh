#!/bin/bash

# İzinleri ayarlama ve dosyayı taşımak
sudo chmod +x aniwatch-tr/aniwatch-tr
sudo mv aniwatch-tr/aniwatch-tr /usr/local/bin

# Kaynak dizinini taşımak
sudo mv aniwatch-tr ~/.aniwatch-tr_src

# İzinleri ayarlamak
sudo chmod 777 ~/.aniwatch-tr_src
sudo chmod 777 ~/.aniwatch-tr_src/*

# Sanal ortamı oluşturup gerekli paketleri yüklemek
cd ~/.aniwatch-tr_src || { echo "Dizin mevcut değil: ~/.aniwatch-tr_src"; exit 1; }
python3 -m venv .venv

# Gereken Python paketlerini yükleme
.venv/bin/pip install requests inquirer

echo "Kurulum tamamlandı. Artık 'aniwatch-tr' komutunu kullanabilirsiniz."
