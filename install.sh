#!/bin/bash

PROJECT_DIR="$HOME/.aniwatch-tr"

if [ -d "$PROJECT_DIR" ]; then
    cd "$PROJECT_DIR" || { echo "Dizin '$PROJECT_DIR' mevcut değil."; exit 1; }

    # Dosyaya çalıştırılabilir izinler verin
    chmod +x "$PROJECT_DIR/aniwatch-tr"

    # Sanal ortam oluşturun
    python3 -m venv .venv

    # Sanal ortamı aktive edin ve gerekli paketleri yükleyin
    source .venv/bin/activate
    pip install requests inquirer

    echo "Kurulum tamamlandı."
else
    echo "Hata: '$PROJECT_DIR' dizini mevcut değil."
    exit 1
fi
