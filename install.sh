#!/bin/bash

# İzinleri ayarlama ve dosyayı taşımak
if [ -f aniwatch-tr/aniwatch-tr ]; then
  sudo chmod +x aniwatch-tr/aniwatch-tr
  sudo mv aniwatch-tr/aniwatch-tr /usr/local/bin
else
  echo "Dosya bulunamadı: aniwatch-tr/aniwatch-tr"
  exit 1
fi

# Kaynak dizinini taşımak
if [ -d aniwatch-tr ]; then
  sudo mv aniwatch-tr ~/.aniwatch-tr
else
  echo "Dizin bulunamadı: aniwatch-tr"
  exit 1
fi

# İzinleri ayarlamak
sudo chmod 755 ~/.aniwatch-tr
sudo chmod 755 ~/.aniwatch-tr/*

# Gereken Python paketlerini yükleme
if [ -f ~/.aniwatch-tr/requirements.txt ]; then
  pip install -r ~/.aniwatch-tr/requirements.txt
else
  echo "requirements.txt dosyası bulunamadı: ~/.aniwatch-tr/requirements.txt"
  exit 1
fi

echo "Kurulum tamamlandı. Artık 'aniwatch-tr' komutunu kullanabilirsiniz."
