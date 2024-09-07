#!/bin/bash

# Klonlanmış dizine geçiş yap
cd aniwatch-tr

# Klonlanmış dizine geçiş yap
cd aniwatch-tr

# Sanal ortam oluştur ve etkinleştir
echo "Sanal ortam oluşturuluyor..."
python3 -m venv venv

echo "Sanal ortam etkinleştiriliyor..."
source venv/bin/activate

# Gerekli Python paketlerini yükle
echo "Python paketleri yükleniyor..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Kurulum Tamamlandı Terminale 'aniwatch-tr' Yazarak, Çalıştırabilirsiniz."
