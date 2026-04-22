"""
Script de préparation du Dataset ML

Ce script :
1. Parcourt les dossiers de data/raw
2. Extrait le texte de chaque page
3. Ne garde que les pages significatives (> 200 caractères)
4. Enregistre le tout dans un CSV pour scikit-learn
"""

import pandas as pd
from pathlib import Path
from src.extractor import extract_document
import os

def build_dataset(raw_dir="data/raw", output_file="data/dataset.csv"):
    raw_dir = Path(raw_dir)
    data = []

    # Parcourir chaque sous-dossier (chaque sous-dossier est une CLASSE)
    for category_dir in raw_dir.iterdir():
        if category_dir.is_dir():
            label = category_dir.name
            print(f"Traitement de la catégorie : {label}")

            for pdf_path in category_dir.glob("*.pdf"):
                print(f"  Extraction : {pdf_path.name}")
                try:
                    # On extrait les pages (on limite à 50 pages par doc pour l'entraînement)
                    pages = extract_document(pdf_path, max_pages=50)
                    
                    for p in pages:
                        # FILTRE DE QUALITÉ : 
                        # On ne garde la page que si elle est assez riche en texte
                        if p['n_chars'] > 200:
                            data.append({
                                "text": p['text'],
                                "label": label,
                                "source": pdf_path.name
                            })
                except Exception as e:
                    print(f"  Erreur sur {pdf_path.name}: {e}")

    # Sauvegarde en CSV
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\n✅ Dataset créé : {len(df)} pages enregistrées dans {output_file}")

if __name__ == "__main__":
    # Installation de pandas si nécessaire
    # pip install pandas
    build_dataset()