"""
Step 5 — Validator (Final)
"""

def is_luhn_valid(number: str) -> bool:
    """Algorithme de Luhn strict pour SIRET."""
    if not number or not number.isdigit() or len(number) != 14:
        return False
    digits = [int(d) for d in number]
    for i in range(len(digits) - 2, -1, -2):
        val = digits[i] * 2
        digits[i] = val if val < 10 else val - 9
    return sum(digits) % 10 == 0

def validate_siret(siret: str) -> bool:
    """Alias pour la validation SIRET."""
    return is_luhn_valid(siret)

def validate_iban(iban: str) -> bool:
    """Valide un IBAN selon la norme ISO 13616."""
    if not iban:
        return False
    iban = iban.replace(" ", "").upper()
    if len(iban) != 27:
        return False
    rearranged = iban[4:] + iban[:4]
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