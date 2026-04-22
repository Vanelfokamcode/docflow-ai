"""
Tests unitaires pour l'extracteur d'entités.
On simule des textes de factures pour vérifier la précision des Regex.
"""

from src.entity_extractor import extract_siret, extract_iban, extract_amounts

def test_extract_siret_simple():
    text = "Mon entreprise est la SASU DATA, SIRET 123 456 789 00012 à Paris."
    assert extract_siret(text) == "12345678900012"

def test_extract_iban_with_spaces():
    text = "Veuillez payer sur l'IBAN : FR76 1234 5678 9012 3456 7890 123"
    assert extract_iban(text) == "FR7612345678901234567890123"

def test_extract_amounts_mixed():
    text = "Total HT : 1 000,50 € / TVA : 200,10€ / Total TTC : 1200.60 EUR"
    amounts = extract_amounts(text)
    assert 1200.60 in amounts
    assert 1000.50 in amounts
    assert amounts[0] == 1200.60 # Le plus gros en premier

def test_no_data():
    text = "Ceci est un texte sans aucune donnée bancaire."
    assert extract_siret(text) is None
    assert extract_iban(text) is None
    assert extract_amounts(text) == []