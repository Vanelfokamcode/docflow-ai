# src/extractor.py
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from pathlib import Path
from src.detector import detect_pdf_type

def extract_page_native(page) -> str:
    text = page.extract_text()
    return text.strip() if text else ""

def extract_page_scanned(image) -> str:
    return pytesseract.image_to_string(image, lang="fra+eng", config="--psm 1").strip()

def extract_document(filepath: str | Path, max_pages: int = None) -> list[dict]:
    filepath = Path(filepath)
    pdf_type = detect_pdf_type(filepath)
    pages_data = []

    if pdf_type == "native":
        with pdfplumber.open(filepath) as pdf:
            pages = pdf.pages[:max_pages] if max_pages else pdf.pages
            for i, page in enumerate(pages, start=1):
                text = extract_page_native(page)
                pages_data.append({
                    "page_num": i,
                    "text": text,
                    "method": "native",
                    "n_chars": len(text),
                    "filename": filepath.name,
                })
    else:
        print(f"  PDF scanné détecté — OCR sur {max_pages if max_pages else 'toutes'} pages...")
        # On ne convertit QUE les pages nécessaires pour économiser la RAM
        images = convert_from_path(filepath, dpi=200, last_page=max_pages)

        for i, image in enumerate(images, start=1):
            text = extract_page_scanned(image)
            pages_data.append({
                "page_num": i,
                "text": text,
                "method": "scanned",
                "n_chars": len(text),
                "filename": filepath.name,
            })
    return pages_data

def extract_all_documents(raw_dir: str | Path, max_pages_per_doc: int = 5) -> list[dict]:
    raw_dir = Path(raw_dir)
    all_pages = []
    for pdf_path in sorted(raw_dir.rglob("*.pdf")):
        classe = pdf_path.parent.name
        try:
            # On limite à 5 pages par doc pour le moment
            pages = extract_document(pdf_path, max_pages=max_pages_per_doc)
            for page in pages:
                page["classe"] = classe
            all_pages.extend(pages)
        except Exception as e:
            print(f"  ERREUR sur {pdf_path.name} : {e}")
    return all_pages