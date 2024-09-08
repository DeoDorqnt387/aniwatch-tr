#!/bin/bash

# Proje dizinini tanımlayalım
PROJECT_DIR="$HOME/.aniwatch-tr"

# Proje dizinine gidip izinleri ayarlayalım
chmod +x $PROJECT_DIR/aniwatch-tr.py

# Python sanal ortamını oluşturup gerekli paketleri yükleyelim
cd $PROJECT_DIR
python3 -m venv .venv
.venv/bin/pip install requests inquirer

sudo chmod +x /usr/local/bin/aniwatch-tr

echo "Kurulum tamamlandı. 'aniwatch-tr' komutunu kullanarak projeyi çalıştırabilirsiniz."
