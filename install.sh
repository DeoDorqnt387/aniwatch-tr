#!/bin/bash

# Proje dizinini tanımlayalım
PROJECT_DIR="$HOME/.aniwatch-tr"

# İzinleri ayarlayalım
chmod +x $PROJECT_DIR/main.py
chmod 755 $PROJECT_DIR
chmod 755 $PROJECT_DIR/*

# Python sanal ortamı oluşturulacak ve gerekli paketler yüklenecek
cd $PROJECT_DIR
python3 -m venv .venv
.venv/bin/pip install requests inquirer

# Komut dosyasını sistem genelinde erişilebilir yapalım
echo -e '#!/bin/bash\n'\
'. '$PROJECT_DIR'/.venv/bin/python '$PROJECT_DIR'/main.py' | sudo tee /usr/local/bin/aniwatch-tr
sudo chmod +x /usr/local/bin/aniwatch-tr

echo "Kurulum tamamlandı. 'aniwatch-tr' komutunu kullanarak projeyi çalıştırabilirsiniz."
