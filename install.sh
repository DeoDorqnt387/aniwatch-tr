#!/bin/bash

# Proje dizinini tanımlayalım
PROJECT_DIR="$HOME/.aniwatch-tr"

# Proje dizinine gidip izinleri ayarlayalım
chmod +x $PROJECT_DIR/main.py
chmod 755 $PROJECT_DIR
chmod 755 $PROJECT_DIR/*

# Python sanal ortamını oluşturup gerekli paketleri yükleyelim
cd $PROJECT_DIR
python3 -m venv .venv
.venv/bin/pip install requests inquirer

# Sanal ortamın yolunu PATH değişkenine ekleyelim
if ! grep -q 'export PATH="$HOME/.aniwatch-tr/.venv/bin:$PATH"' ~/.bashrc; then
    echo 'export PATH="$HOME/.aniwatch-tr/.venv/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc
fi

# Komut dosyasını sistem genelinde erişilebilir yapalım
echo -e '#!/bin/bash\n'\
'~/.aniwatch-tr/.venv/bin/python ~/.aniwatch-tr/main.py' | sudo tee /usr/local/bin/aniwatch-tr
sudo chmod +x /usr/local/bin/aniwatch-tr

echo "Kurulum tamamlandı. 'aniwatch-tr' komutunu kullanarak projeyi çalıştırabilirsiniz."
