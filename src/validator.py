"""
Step 5 — Validator (Version Robuste)

Ce module implémente les validations mathématiques strictes (ISO 7064 et ISO 13616).
"""

def validate_iban(iban: str) -> bool:
    """
    Valide un IBAN selon la norme ISO 13616.
    
    Algorithme :
    1. Vérifier la longueur (27 pour la France).
    2. Déplacer les 4 premiers caractères à la fin.
    3. Remplacer les lettres par des chiffres (A=10, ..., Z=35).
    4. Vérifier que le modulo 97 du nombre obtenu est égal à 1.
    """
    if not iban:
        return False
        
    # Nettoyage
    iban = iban.replace(" ", "").upper()
    
    # Longueur standard FR = 27 (on peut élargir si on accepte l'étranger : 15 à 34)
    if len(iban) != 27:
        return False

    # 1. Déplacer les 4 premiers caractères à la fin
    # Exemple : FR76 1234... -> 1234...FR76
    rearranged = iban[4:] + iban[:4]
    
    # 2. Remplacer les lettres par des chiffres
    numeric_str = ""
    for char in rearranged:
        if char.isdigit():
            numeric_str += char
        else:
            # A=10, B=11... via le code ASCII
            numeric_str += str(ord(char) - ord('A') + 10)
            
    # 3. Modulo 97
    try:
        return int(numeric_str) % 97 == 1
    except ValueError:
        return False

def is_luhn_valid(number: str) -> bool:
    """Algorithme de Luhn strict pour SIRET."""
    if not number or not number.isdigit() or len(number) != 14:
        return False
    digits = [int(d) for d in number]
    # On multiplie par 2 un chiffre sur deux en partant de la droite
    for i in range(len(digits) - 2, -1, -2):
        val = digits[i] * 2
        digits[i] = val if val < 10 else val - 9
    return sum(digits) % 10 == 0

def validate_amount_consistency(amounts: list[float]) -> bool:
    """Vérifie la relation HT + TVA = TTC (Tolérance 0.05)."""
    if len(amounts) < 3:
        return False
    top = sorted(list(set(amounts)), reverse=True)[:10]
    for i, total in enumerate(top):
        for j, a in enumerate(top):
            for k, b in enumerate(top):
                if i != j and i != k and j != k:
                    if abs(total - (a + b)) < 0.05:
                        return True
    return False