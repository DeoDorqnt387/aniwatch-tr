#!/bin/bash

# Proje dizinini tanımlayalım
PROJECT_DIR="$HOME/.aniwatch-tr"

# İzinleri ayarlayalım
chmod +x $PROJECT_DIR/main.py  # Buraya çalıştırmak istediğiniz Python dosyasının yolunu ekleyin
chmod 777 $PROJECT_DIR
chmod 777 $PROJECT_DIR/*

# Python sanal ortamı oluşturalım ve gerekli paketleri yükleyelim
cd $PROJECT_DIR
python3 -m venv .venv
.venv/bin/pip install requests inquirerpy

# Komut dosyasını sistem genelinde erişilebilir yapalım
echo -e '#!/bin/bash\n. '$PROJECT_DIR'/.venv/bin/python '$PROJECT_DIR'/main.py' | sudo tee /usr/local/bin/aniwatch-tr
sudo chmod +x /usr/local/bin/aniwatch-tr

echo "Kurulum tamamlandı. 'aniwatch-tr' komutunu kullanarak projeyi çalıştırabilirsiniz."
