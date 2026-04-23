import pandas as pd
import joblib
import re
from pathlib import Path

# On garde la fonction d'augmentation pour l'entraînement
def augment_text_with_signals(text):
    signals = []
    text_upper = str(text).upper()
    if "FACTURE" in text_upper or "INVOICE" in text_upper:
        signals.append("FEATURE_KEYWORD_INVOICE")
    if re.search(r"FR\d{2}[A-Z0-9]{23}", text_upper.replace(" ", "")):
        signals.append("FEATURE_HAS_IBAN")
    return " ".join(signals) + " " + str(text)

def smart_predict(text, model):
    """
    Système de décision hybride (Règles Métier + Machine Learning).
    C'est cette approche qui est utilisée en production bancaire.
    """
    text_upper = str(text).upper()
    text_no_space = text_upper.replace(" ", "").replace("\n", "")
    
    # 🚩 RÈGLE D'OR 1 : Si on a un IBAN et le mot FACTURE -> C'est une facture.
    has_iban = re.search(r"FR\d{2}[A-Z0-9]{23}", text_no_space)
    has_invoice_keyword = "FACTURE" in text_upper or "INVOICE" in text_upper
    
    if has_iban and has_invoice_keyword:
        return "facture", 0.99  # On force la décision avec 99% de confiance
    
    # 🚩 RÈGLE D'OR 2 : Si c'est un Bulletin de Salaire Urssaf (mots clés spécifiques)
    if "BULLETIN DESALAIRE" in text_no_space or "COTISATIONS SOCIALES" in text_upper:
        return "bulletin_paie", 0.98

    # 🚩 SINON : On laisse le modèle ML décider
    text_augmented = augment_text_with_signals(text)
    prediction = model.predict([text_augmented])[0]
    probs = model.predict_proba([text_augmented])[0]
    confidence = max(probs)
    
    return prediction, confidence