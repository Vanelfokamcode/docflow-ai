"""
Step 2 bis — Prepare ML Data (Version Haute-Fidélité)

Ce script parcourt le dossier data/raw, extrait le texte de chaque PDF 
(via texte natif ou OCR si nécessaire) et sauvegarde le tout dans un format 
propre pour l'entraînement du modèle de Machine Learning.

Optimisations :
- Basse consommation RAM (traitement page par page).
- Nettoyage automatique de la mémoire (gc.collect).
- Mixte Natif/OCR intelligent.
"""

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import gc
import pdfplumber

def ocr_page(pdf_path, page_num):
    """
    Extrait le texte d'une page spécifique via OCR de manière isolée.
    On ouvre et ferme le document à chaque fois pour libérer la RAM.
    """
    try:
        doc = fitz.open(pdf_path)
        page = doc.load_page(page_num)
        
        # Rendu de la page en image (DPI 150 = bon compromis précision/mémoire)
        pix = page.get_pixmap(matrix=fitz.Matrix(150/72, 150/72))
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        
        # OCR via Tesseract
        text = pytesseract.image_to_string(img, lang='fra+eng')
        
        # Libération immédiate des ressources
        doc.close()
        del img, pix, img_data
        return text.strip()
    except Exception as e:
        return ""

def extract_smart(pdf_path, max_pages=30):
    """
    Tente l'extraction native (pdfplumber), 
    sinon bascule sur l'OCR page par page.
    """
    pages_data = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            pages_to_process = min(max_pages, total_pages)
            
            for i in range(pages_to_process):
                page = pdf.pages[i]
                text = page.extract_text()
                
                # Si on extrait plus de 100 caractères, on considère le texte comme valide (Natif)
                if text and len(text.strip()) > 100:
                    pages_data.append({
                        "page_num": i + 1,
                        "text": text.strip(),
                        "method": "native"
                    })
                else:
                    # Sinon, on tente l'OCR pour cette page spécifique
                    ocr_text = ocr_page(pdf_path, i)
                    if len(ocr_text) > 20:
                        pages_data.append({
                            "page_num": i + 1,
                            "text": ocr_text,
                            "method": "scanned"
                        })
                
                # Nettoyage mémoire après chaque page
                gc.collect()
                
    except Exception as e:
        print(f"⚠️ Erreur lors de l'ouverture de {pdf_path.name}: {e}")
        
    return pages_data

def run():
    raw_dir = Path("data/raw")
    all_data = []
    
    if not raw_dir.exists():
        print(f"❌ Erreur : Le dossier {raw_dir} n'existe pas.")
        return

    print("🚀 Démarrage de l'extraction Haute-Fidélité (Natif + OCR)...")
    
    # On parcourt les sous-dossiers (chaque dossier est une classe)
    folders = sorted([d for d in raw_dir.iterdir() if d.is_dir()])
    
    for class_folder in folders:
        label = class_folder.name
        files = list(class_folder.glob("*.pdf"))
        
        if not files:
            continue
            
        print(f"\n📁 Dossier : {label} ({len(files)} fichiers)")
        
        for pdf_path in tqdm(files, desc=f"Extraction {label}"):
            # On définit des limites intelligentes pour équilibrer le dataset
            # Un rapport annuel a beaucoup de pages, une facture très peu.
            if label == "rapport_annuel":
                limit = 20
            elif label == "facture":
                limit = 3 # Les factures font souvent 1 ou 2 pages
            else:
                limit = 10
            
            results = extract_smart(pdf_path, max_pages=limit)
            
            for res in results:
                all_data.append({
                    "text": res["text"],
                    "label": label,  # Nom de la catégorie
                    "method": res["method"],
                    "source": pdf_path.name
                })
            
            # Forcer le nettoyage après chaque document
            gc.collect()

    # Sauvegarde des résultats
    if all_data:
        df = pd.DataFrame(all_data)
        
        # Création du dossier processed s'il n'existe pas
        output_dir = Path("data/processed")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Sauvegarde au format attendu par le classificateur
        output_path = output_dir / "annotations.csv"
        df.to_csv(output_path, index=False)
        
        print(f"\n✅ Dataset créé avec succès : {len(df)} pages enregistrées.")
        print(f"📍 Chemin : {output_path}")
        print("\nRépartition par classe et méthode :")
        print(df.groupby(['label', 'method']).size())
    else:
        print("❌ Aucune donnée n'a pu être extraite. Vérifie tes fichiers PDF.")

if __name__ == "__main__":
    run()