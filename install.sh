#!/bin/bash

# İzinleri ayarlama ve dosyayı taşımak
sudo chmod +x aniwatch-tr
sudo mv aniwatch-tr /usr/local/bin/

sudo cp -r ~/aniwatch-tr /usr/local/aniwatch-tr
sudo chmod +x /usr/local/aniwatch-tr/main.py

pip install -r requirements.txt

echo "Kurulum tamamlandı. Artık 'aniwatch-tr' komutunu kullanabilirsiniz."
