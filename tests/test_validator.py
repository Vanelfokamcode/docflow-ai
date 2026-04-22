# tests/test_validator.py
from src.validator import validate_iban, is_luhn_valid

def test_iban_valid_fr():
    # Cet IBAN est mathématiquement correct (Modulo 97 = 1)
    valid_iban = "FR1430001007941234567890123"
    assert validate_iban(valid_iban) == True  # <--- Vérifie bien cette ligne

def test_iban_invalid_key():
    invalid_iban = "FR7630006000011234567890115"
    assert validate_iban(invalid_iban) == False

def test_siret_lvmh_real():
    assert is_luhn_valid("77567041700010") == True

def test_siret_fake():
    assert is_luhn_valid("12345678901234") == False