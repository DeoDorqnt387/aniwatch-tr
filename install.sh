#!/bin/bash

# Gerekli izinleri verelim
sudo chmod +x ~/.aniwatch-tr
sudo chmod 777 ~/.aniwatch-tr

# Sanal ortamı oluşturalım
cd ~/.aniwatch-tr && sudo python3 -m venv .venv

# Gerekli paketleri yükleyelim
cd ~/.aniwatch-tr && sudo .venv/bin/pip install requests inquirer

# Kullanıcıya `aniwatch-tr` komutunu çalıştırabilmesi için gerekli ayarları yapalım
echo -e '#!/bin/bash\ncd ~/.aniwatch-tr && .venv/bin/python aniwatch_tr.py' | sudo tee /usr/local/bin/aniwatch-tr
sudo chmod +x /usr/local/bin/aniwatch-tr

echo "Kurulum tamamlandı. 'aniwatch-tr' komutunu kullanarak projeyi çalıştırabilirsiniz."
