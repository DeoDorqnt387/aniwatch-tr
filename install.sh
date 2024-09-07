#!/bin/bash

# Proje dizinine geç
cd "$(dirname "$0")"

# Python sanal ortamını oluştur
python3 -m venv .venv

# Sanal ortamı aktif et
source .venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Python dosyasına çalıştırma izni ver
chmod +x main.py

# Programı /usr/local/bin dizinine sembolik link oluştur
cat << EOF | sudo tee /usr/local/bin/aniwatch-tr > /dev/null
#!/bin/bash
source $(pwd)/.venv/bin/activate
exec python3 $(pwd)/main.py "\$@"
EOF

# Betiğe çalıştırma izni ver
sudo chmod +x /usr/local/bin/aniwatch-tr

echo "Kurulum tamamlandı. 'aniwatch-tr' komutunu kullanarak programı çalıştırabilirsiniz."
