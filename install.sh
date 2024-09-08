#!/bin/bash

# Proje dizinini tanımlayalım
PROJECT_DIR="$HOME/.aniwatch-tr"

# Proje dizinine gidip izinleri ayarlayalım
chmod +x $PROJECT_DIR/aniwatch-tr.py
chmod 755 $PROJECT_DIR
chmod 755 $PROJECT_DIR/*

# Python sanal ortamını oluşturup gerekli paketleri yükleyelim
cd $PROJECT_DIR
python3 -m venv .venv
.venv/bin/pip install requests inquirer

# Komut dosyasını sistem genelinde erişilebilir yapalım
echo -e '#!/bin/bash\n'\
'~/.aniwatch-tr/.venv/bin/python ~/.aniwatch-tr/main.py' | sudo tee /usr/local/bin/aniwatch-tr
sudo chmod +x /usr/local/bin/aniwatch-tr

echo "Kurulum tamamlandı. 'aniwatch-tr' komutunu kullanarak projeyi çalıştırabilirsiniz."
