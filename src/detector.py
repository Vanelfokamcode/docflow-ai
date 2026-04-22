# src/detector.py
import pdfplumber
from pathlib import Path

NATIVE_THRESHOLD = 20  # Très bas pour détecter même une petite ligne de texte
PAGES_TO_CHECK = 5     # On regarde un peu plus loin dans le doc

def detect_pdf_type(filepath: str | Path) -> str:
    filepath = Path(filepath)
    try:
        with pdfplumber.open(filepath) as pdf:
            total_pages = len(pdf.pages)
            pages_to_check = min(PAGES_TO_CHECK, total_pages)

            for i in range(pages_to_check):
                text = pdf.pages[i].extract_text() or ""
                if len(text.strip()) > NATIVE_THRESHOLD:
                    return "native" # On a trouvé du texte, c'est natif !
            
            return "scanned" # Aucune des premières pages n'a de texte
    except Exception as e:
        return "scanned" # Par sécurité