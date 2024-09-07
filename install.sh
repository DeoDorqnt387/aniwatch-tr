#!/bin/bash

# Gerekli izinleri ayarla ve komut dosyasını /usr/local/bin'e taşı
sudo chmod +x aniwatch-tr/aniwatch-tr
sudo mv aniwatch-tr/aniwatch-tr /usr/local/bin/aniwatch-tr

# Proje klasörünü home dizinine taşı ve gerekli izinleri ayarla
sudo mv .aniwatch-tr ~/.aniwatch-tr
sudo chmod 777 ~/.aniwatch-tr
sudo chmod 777 ~/.aniwatch-tr/*

# Sanal ortam oluştur ve bağımlılıkları yükle
cd ~/.aniwatch_src && sudo python3 -m venv .venv
cd ~/.aniwatch_src && sudo .venv/bin/pip install requests inquirer

echo "Kurulum tamamlandı. 'aniwatch-tr' komutunu kullanarak programı çalıştırabilirsiniz."
