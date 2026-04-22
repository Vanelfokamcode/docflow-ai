# tests/test_extractor.py
import pytest
from pathlib import Path
from src.detector import detect_pdf_type
from src.extractor import extract_document

# On récupère le premier PDF trouvé dans n'importe quel dossier de data/raw
TEST_PDF = next(Path("data/raw").rglob("*.pdf"), None)

def test_pdf_exists():
    assert TEST_PDF is not None, "Aucun PDF trouvé. Lance scripts/download_data.py"

def test_detect_type_returns_valid_value():
    result = detect_pdf_type(TEST_PDF)
    assert result in ("native", "scanned")

def test_extract_document_returns_list():
    # max_pages est CRITIQUE ici pour éviter le "Killed"
    pages = extract_document(TEST_PDF, max_pages=2)
    assert isinstance(pages, list)
    assert len(pages) > 0

def test_extract_document_page_structure():
    # max_pages est CRITIQUE ici aussi
    pages = extract_document(TEST_PDF, max_pages=2)
    required_keys = {"page_num", "text", "method", "n_chars", "filename"}
    for page in pages:
        assert required_keys.issubset(page.keys())

def test_extract_document_text_not_empty():
    pages = extract_document(TEST_PDF, max_pages=2)
    # On vérifie qu'au moins une page a du texte (si c'est un doc natif)
    if detect_pdf_type(TEST_PDF) == "native":
        texts = [p["text"] for p in pages if p["n_chars"] > 10]
        assert len(texts) > 0