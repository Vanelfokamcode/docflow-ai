"""
DocFlow AI - Interface Utilisateur
"""
import streamlit as st
import joblib
import os
from src.extractor import extract_document
from src.entity_extractor import extract_siret, extract_iban
from src.validator import validate_siret, validate_iban
from src.agent import DocAgent

# Configuration de la page
st.set_page_config(page_title="DocFlow AI", layout="wide", page_icon="🏦")

st.title("🏦 DocFlow AI")
st.markdown("### Analyse Intelligente de Documents Financiers")

# Chargement du modèle et de l'agent
@st.cache_resource
def load_resources():
    model = joblib.load("storage/model.joblib")
    agent = DocAgent()
    return model, agent

try:
    model, agent = load_resources()
except:
    st.error("⚠️ Modèle non trouvé. Lance src/classifier.py d'abord.")
    st.stop()

# Barre latérale pour l'upload
with st.sidebar:
    st.header("1. Chargement")
    uploaded_file = st.file_uploader("Déposez un PDF financier", type="pdf")
    st.divider()
    st.info("Traitement 100% Local & Sécurisé")

if uploaded_file:
    # Sauvegarde temporaire du fichier
    temp_path = f"temp_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # --- ÉTAPE 1 : PIPELINE TECHNIQUE ---
    with st.spinner("Analyse technique en cours..."):
        # On extrait les 5 premières pages pour la vitesse
        pages = extract_document(temp_path, max_pages=5)
        full_text = " ".join([p['text'] for p in pages])
        
        # Classification ML
        doc_type = model.predict([full_text])[0]
        
        # Extraction & Validation
        siret = extract_siret(full_text)
        iban = extract_iban(full_text)

    # --- ÉTAPE 2 : AFFICHAGE DES RÉSULTATS ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Catégorie détectée", doc_type.upper())
    
    with col2:
        val_siret = "✅" if siret and validate_siret(siret) else "❌"
        st.metric("SIRET", siret if siret else "Non trouvé", val_siret)
        
    with col3:
        val_iban = "✅" if iban and validate_iban(iban) else "❌"
        st.metric("IBAN", "Détecté" if iban else "Absent", val_iban)

    st.divider()

    # --- ÉTAPE 3 : INTERACTION IA ---
    st.subheader("💬 Posez une question à l'IA sur ce document")
    user_query = st.text_input("Exemple : Résume ce document, Quel est le montant total, etc.")
    
    if user_query:
        with st.spinner("L'IA analyse le contenu..."):
            response = agent.ask(full_text, user_query)
            st.chat_message("assistant").write(response)

    # Nettoyage
    os.remove(temp_path)
else:
    st.info("Veuillez uploader un document PDF dans la barre latérale pour démarrer l'analyse.")