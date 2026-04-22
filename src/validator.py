"""
Step 5 — Validator (Final)
"""

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

def validate_siret(siret: str) -> bool:
    """Valide un SIRET (14 chiffres + Luhn)."""
    return is_luhn_valid(siret)

def validate_iban(iban: str) -> bool:
    """
    Valide un IBAN selon la norme ISO 13616.
    Format FR: 27 caractères.
    """
    if not iban:
        return False
    
    iban = iban.replace(" ", "").upper()
    
    if len(iban) != 27:
        return False

    # Déplacer les 4 premiers caractères à la fin
    rearranged = iban[4:] + iban[:4]
    
    # Remplacer les lettres par des chiffres
    numeric_str = ""
    for char in rearranged:
        if char.isdigit():
            numeric_str += char
        else:
            numeric_str += str(ord(char) - ord('A') + 10)
            
    try:
        return int(numeric_str) % 97 == 1
    except ValueError:
        return False
