# scripts/prepare_ml_data.py
"""
Version optimisée en mémoire pour préparer le dataset DocFlow AI
"""

from pathlib import Path
import pandas as pd
from tqdm import tqdm
import gc

from src.extractor import extract_document

def prepare_ml_dataset(max_pages_per_doc=80):
    raw_dir = Path("data/raw")
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)

    all_pages = []
    total_processed = 0

    print("🚀 Début de l'extraction des PDFs (version optimisée mémoire)\n")

    for class_dir in sorted(raw_dir.iterdir()):
        if not class_dir.is_dir():
            continue

        classe = class_dir.name
        pdf_files = list(class_dir.glob("*.pdf"))

        print(f"📁 Classe '{classe}' — {len(pdf_files)} PDFs")

        for pdf_path in tqdm(pdf_files, desc=classe):
            try:
                # Limite le nombre de pages pour les très gros documents
                pages = extract_document(pdf_path)
                
                # On limite à max_pages_per_doc pour éviter les crashes
                if len(pages) > max_pages_per_doc:
                    print(f"   ⚠️ {pdf_path.name} a {len(pages)} pages → on limite à {max_pages_per_doc}")
                    pages = pages[:max_pages_per_doc]

                for page in pages:
                    text = page.get("text", "").strip()
                    if len(text) > 30:   # ignore pages presque vides
                        all_pages.append({
                            "filename": pdf_path.name,
                            "page_num": page.get("page_num"),
                            "text": text,
                            "classe": classe,
                            "method": page.get("method", "unknown"),
                            "n_chars": len(text)
                        })
                        total_processed += 1

                # Nettoyage mémoire
                del pages
                gc.collect()

            except Exception as e:
                print(f"   ❌ Erreur sur {pdf_path.name} : {e}")

    if not all_pages:
        print("❌ Aucun texte extrait. Vérifie tes PDFs.")
        return None

    df = pd.DataFrame(all_pages)

    output_file = processed_dir / "annotations.csv"
    df.to_csv(output_file, index=False)

    print("\n" + "="*80)
    print("✅ DATASET CRÉÉ AVEC SUCCÈS (version optimisée)")
    print("="*80)
    print(f"Total pages sauvegardées : {len(df)}")
    print(f"Fichier : {output_file}")
    print("\nRépartition par classe :")
    print(df['classe'].value_counts().sort_index())

    return df


if __name__ == "__main__":
    prepare_ml_dataset(max_pages_per_doc=30)   # ajuste à 60 si ça tue encore