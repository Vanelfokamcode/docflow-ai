# src/entity_extractor.py
import re

def extract_siret(text: str) -> str | None:
    """
    Extrait un SIRET de 14 chiffres de manière flexible.
    Gère : SIRET : 123 456..., SIRET 123.456..., SIRET:123456...
    """
    if not text:
        return None
    
    # 1. Recherche par mot-clé (la plus fiable)
    # On cherche "SIRET" suivi de n'importe quoi (espaces, :, -, .) puis 14 chiffres
    pattern_keyword = r"SIRET\s*[:\-\s\.]*([\d\s\.\-]{14,25})"
    match = re.search(pattern_keyword, text, re.IGNORECASE)
    
    if match:
        # On extrait la partie numérique et on nettoie tout sauf les chiffres
        raw_digits = match.group(1)
        clean_digits = re.sub(r"[^\d]", "", raw_digits)
        if len(clean_digits) >= 14:
            return clean_digits[:14]

    # 2. Recherche par bloc de 14 chiffres (si le mot SIRET est absent ou mal lu)
    # On supprime d'abord les espaces dans le texte pour coller les chiffres
    text_no_space = re.sub(r"\s", "", text)
    all_14_digits = re.findall(r"\d{14}", text_no_space)
    
    for potential in all_14_digits:
        # Ici, on pourrait ajouter une validation Luhn pour confirmer
        return potential

    return None

def extract_iban(text: str) -> str | None:
    """Extrait un IBAN français (FR + 25 carac)."""
    if not text:
        return None
    
    # Nettoyage des espaces pour la recherche
    clean_text = text.replace(" ", "").replace("\n", "")
    pattern = r"FR\d{2}[A-Z0-9]{23}"
    match = re.search(pattern, clean_text)
    
    if match:
        return match.group(0)
    return None

def extract_amounts(text: str) -> list[float]:
    """Extrait les montants financiers."""
    if not text:
        return []
    
    # Cherche les chiffres suivis de € ou EUR
    pattern = r"(\d[\d\s,.]*)[\s]*(?:€|EUR|Euros)"
    matches = re.findall(pattern, text, re.IGNORECASE)
    
    found = []
    for m in matches:
        try:
            # Nettoyage FR (1 250,50 -> 1250.50)
            val = m.replace(" ", "").replace(",", ".")
            if val.count('.') > 1:
                parts = val.split('.')
                val = "".join(parts[:-1]) + "." + parts[-1]
            found.append(float(val))
        except:
            continue
    return sorted(list(set(found)), reverse=True)