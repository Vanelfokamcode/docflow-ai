"""
Step 4 — Entity Extractor

Ce module utilise les Expressions Régulières (Regex) pour extraire
des données structurées spécifiques aux documents financiers.

Regex utilisées :
- SIRET : 14 chiffres (on gère les espaces)
- IBAN : Format FR + 25 caractères
- Montants : Nombres suivis du symbole monétaire
"""

import re

def extract_siret(text: str) -> str | None:
    """
    Cherche un SIRET (14 chiffres) dans le texte.
    On nettoie les espaces car les SIRET sont souvent écrits '123 456...'
    """
    if not text:
        return None
    
    # On cherche d'abord des séquences de chiffres avec des espaces
    # ex: "432 345 678 00012"
    potential_siret = re.findall(r'\d[\d\s]{13,20}\d', text)
    
    for s in potential_siret:
        clean_s = re.sub(r'\s', '', s)
        if len(clean_s) == 14:
            return clean_s
    return None

def extract_iban(text: str) -> str | None:
    """
    Cherche un IBAN français.
    Format : FR + 2 chiffres + 23 caractères (souvent par blocs de 4)
    """
    if not text:
        return None
        
    pattern = r'FR\d{2}[ ]\d{4}[ ]\d{4}[ ]\d{4}[ ]\d{4}[ ]\d{4}[ ]\d{3}'
    # On cherche aussi la version sans espaces
    pattern_no_space = r'FR\d{22,25}'
    
    match = re.search(pattern, text) or re.search(pattern_no_space, text)
    
    if match:
        return match.group(0).replace(" ", "")
    return None

def extract_amounts(text: str) -> list[float]:
    if not text:
        return []
        
    # Nouvelle Regex plus large : 
    # - Cherche des nombres
    # - Suivis de : €, EUR, Euros, M€, Md€ (milliards), ou Millions
    pattern = r'(\d[\d\s,.]*)[\s]*(?:€|EUR|Euros|M€|Md€|millions|milliards)'
    matches = re.findall(pattern, text, re.IGNORECASE)
    
    found_amounts = []
    for m in matches:
        try:
            clean_val = m.replace("\s", "").replace(",", ".").strip()
            # On gère le cas des espaces insécables ou bizarres
            clean_val = "".join(clean_val.split())
            
            if clean_val.count('.') > 1:
                parts = clean_val.split('.')
                clean_val = "".join(parts[:-1]) + "." + parts[-1]
            
            val = float(clean_val)
            if val > 0: # On évite les zéros
                found_amounts.append(val)
        except ValueError:
            continue
            
    return sorted(list(set(found_amounts)), reverse=True)