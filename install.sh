#!/bin/bash

# Proje dizinini tanımlayalım
PROJECT_DIR="$HOME/.aniwatch-tr"

# İzinleri ayarlayalım
chmod +x $PROJECT_DIR/main.py
chmod 777 $PROJECT_DIR
chmod 777 $PROJECT_DIR/*

cd ~/.aniwatch-tr && sudo python3 -m venv .venv
cd ~/.aniwatch-tr && sudo .venv/bin/pip install requests inquirer

# Komut dosyasını sistem genelinde erişilebilir yapalım
echo -e '#!/bin/bash\npython3 '$PROJECT_DIR'/aniwatch-tr' | sudo tee /usr/local/bin/doccli
sudo chmod +x /usr/local/bin/aniwatch-tr

echo "Kurulum tamamlandı. 'aniwatch-tr' komutunu kullanarak projeyi çalıştırabilirsiniz."
