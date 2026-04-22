# scripts/download_data.py
import httpx
from pathlib import Path

DOWNLOADS = {
    "rapport_annuel": [
        ("amf_rapport_2024.pdf",
         "https://www.amf-france.org/sites/institutionnel/files/private/2025-05/amf_rapport_annuel_2024_0.pdf"),
        ("amf_rapport_2022.pdf",
         "https://www.amf-france.org/sites/institutionnel/files/private/2024-05/ra_amf_2022_fr.pdf"),
        ("lvmh_rapport_2023.pdf",
         "https://r.lvmh-static.com/uploads/2024/03/lvmh_rapport-annuel-2023.pdf"),
    ]
}

BASE = Path("data/raw")

def download(name: str, url: str, folder: str):
    dest = BASE / folder / name
    if dest.exists():
        print(f"  Déjà téléchargé : {name}")
        return
    print(f"  Téléchargement : {name}...")
    try:
        r = httpx.get(url, timeout=60, follow_redirects=True)
        r.raise_for_status()
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(r.content)
        print(f"  OK — {len(r.content)/1024:.0f} KB")
    except Exception as e:
        print(f"  ERREUR : {e}")

if __name__ == "__main__":
    for folder, files in DOWNLOADS.items():
        print(f"\n--- {folder} ---")
        for name, url in files:
            download(name, url, folder)