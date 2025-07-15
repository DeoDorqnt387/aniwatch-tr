
"""
Aniwatch-TR versiyon kontrol modülü
"""
import json
import requests
from urllib.request import urlopen
from urllib.error import URLError

__version__ = "1.0.0"
__author__ = "DeoDorqnt387"

def current_version():
    """Mevcut aniwatch-tr versiyonunu al"""
    return __version__

def latest_github_version():
    try:
        url = "https://api.github.com/repos/DeoDorqnt387/aniwatch-tr/releases/latest"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data['tag_name'].replace('v', '').replace('V', '')
        return None
    except (requests.RequestException, KeyError):
        return None

def latest_pypi_version():
    try:
        url = "https://pypi.org/pypi/aniwatch-tr/json"
        with urlopen(url, timeout=5) as response:
            data = json.loads(response.read())
            return data['info']['version']
    except (URLError, json.JSONDecodeError, KeyError):
        return None

def version_compare(current, latest):
    if not current or not latest:
        return None
    
    # Versiyon parçalarını ayır
    current_parts = [int(x) for x in current.split('.')]
    latest_parts = [int(x) for x in latest.split('.')]
    
    # Uzunlukları eşitle
    max_len = max(len(current_parts), len(latest_parts))
    current_parts += [0] * (max_len - len(current_parts))
    latest_parts += [0] * (max_len - len(latest_parts))
    
    for i in range(max_len):
        if current_parts[i] < latest_parts[i]:
            if i == 0:
                return "Major"  # Büyük güncelleme
            elif i == 1:
                return "Minor"  # Özellik güncelleme
            else:
                return "Patch"  # Hata düzeltme
        elif current_parts[i] > latest_parts[i]:
            return "Newer"  # Mevcut versiyon daha yeni
    
    return "Same"  # Aynı versiyon

def aniwatch_status():
    current = current_version()
    
    latest = latest_github_version()
    source = "GitHub"
    
    if not latest:
        latest = latest_pypi_version()
        source = "PyPI"
    
    if not latest:
        return f"⚠️ Güncel versiyon kontrol edilemedi (Mevcut: {current})"
    
    comparison = version_compare(current, latest)
    
    if comparison == "Same":
        return f"✅ Aniwatch-TR güncel ({current})"
    elif comparison in ["Major", "Minor", "Patch"]:
        return f"🔄 Aniwatch-TR güncellenebilir ({current} → {latest}) [{comparison}]"
    elif comparison == "Newer":
        return f"🚀 Geliştirme versiyonu ({current} > {latest})"
    else:
        return f"❓ Versiyon karşılaştırılamadı ({current} vs {latest})"

def check_updates():
    print("🔍 Aniwatch-TR güncelleme kontrolü...")
    status = aniwatch_status()
    print(status)
    
    if "güncellenebilir" in status:
        print("\n📥 Güncelleme için:")
        print("   • GitHub: https://github.com/DeoDorqnt387/aniwatch-tr")
        print("   • PyPI: pip install --upgrade aniwatch-tr")