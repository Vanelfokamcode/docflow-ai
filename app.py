import streamlit as st
import joblib
import os
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import re

# Modules personnels
from src.extractor import extract_document
from src.entity_extractor import extract_siret, extract_iban
from src.validator import validate_siret, validate_iban
from src.agent import DocAgent
from src.classifier import augment_text_with_signals

# ============================================================
# CONFIGURATION
# ============================================================
st.set_page_config(page_title="DocFlow AI | Smart Finance", layout="wide", page_icon="🏦")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    .main { background-color: #FAFBFC; font-family: 'Inter', sans-serif; }
    .main-header { background: linear-gradient(135deg, #0066FF 0%, #0052CC 100%); padding: 20px; border-radius: 12px; color: white; margin-bottom: 20px; }
    .section-card { background: white; border: 1px solid #E5E7EB; border-radius: 12px; padding: 20px; margin-bottom: 15px; }
    .status-box { text-align: center; padding: 15px; background: #F0F7FF; border-radius: 10px; }
    .entity-row { display: flex; align-items: center; justify-content: space-between; padding: 10px; background: #F9FAFB; border-radius: 8px; margin-bottom: 5px; border: 1px solid #E5E7EB; }
    .raw-text-box { background: #1E1E1E; color: #D4D4D4; font-family: monospace; padding: 15px; border-radius: 8px; max-height: 300px; overflow-y: auto; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_assets():
    model = joblib.load("storage/model.joblib")
    agent = DocAgent()
    return model, agent

# ============================================================
# BARRE LATÉRALE
# ============================================================
with st.sidebar:
    st.markdown("### 🏦 DocFlow AI Engine")
    uploaded_file = st.file_uploader("📁 Importer un document financier", type=["pdf"])
    st.divider()
    st.info("Système Hybride : Règles Métier + Machine Learning")

# ============================================================
# LOGIQUE PRINCIPALE
# ============================================================
st.markdown('<div class="main-header"><h1>📊 DocFlow AI</h1><p>Intelligence Artificielle de traitement documentaire</p></div>', unsafe_allow_html=True)

try:
    model, agent = load_assets()
except Exception as e:
    st.error(f"❌ Erreur chargement modèle : {e}")
    st.stop()

if uploaded_file:
    temp_path = f"temp_{uploaded_file.name}"
    with Path(temp_path).open("wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("🧠 Analyse chirurgicale en cours..."):
        # 1. Extraction
        pages = extract_document(temp_path, max_pages=5)
        full_text = " ".join([p['text'] for p in pages])
        text_upper = full_text.upper()
        
        # 2. Logique de décision PRIORITAIRE (Business Rules)
        has_facture_keyword = "FACTURE" in text_upper or "INVOICE" in text_upper
        has_iban = re.search(r"FR\d{2}[A-Z0-9]{23}", text_upper.replace(" ", ""))
        
        # On initialise les variables pour éviter le NameError
        probs = None 

        if has_facture_keyword and has_iban:
            prediction = "facture"
            confidence = 99.9
            method = "Règle Métier (IBAN + Mot-clé)"
        elif "BULLETIN" in text_upper and "SALAIRE" in text_upper:
            prediction = "bulletin_paie"
            confidence = 99.8
            method = "Règle Métier (Paie)"
        else:
            # 3. Machine Learning (si pas de règle prioritaire)
            text_augmented = augment_text_with_signals(full_text)
            prediction = model.predict([text_augmented])[0]
            probs = model.predict_proba([text_augmented])[0]
            confidence = max(probs) * 100
            method = "Machine Learning (TF-IDF)"

        # 4. Extraction d'entités
        siret = extract_siret(full_text)
        iban = extract_iban(full_text)
        siret_valid = validate_siret(siret) if siret else False
        iban_valid = validate_iban(iban) if iban else False

    # --- AFFICHAGE ---
    col_left, col_right = st.columns([1, 1.5], gap="large")

    with col_left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("#### 🎯 Classification")
        st.markdown(f"""
            <div class="status-box">
                <div style="font-size: 0.8rem; color: #6B7280; text-transform: uppercase;">Type détecté</div>
                <div style="font-size: 1.6rem; font-weight: 700; color: #0066FF;">{prediction.upper()}</div>
                <div style="font-size: 0.9rem; margin-top:5px;">Méthode : <b>{method}</b></div>
                <div style="font-size: 1.1rem; font-weight: 600; color: #00C853; margin-top:5px;">{confidence:.1f}% confiance</div>
            </div>
        """, unsafe_allow_html=True)
        
        if probs is not None:
            with st.expander("📊 Analyse des probabilités ML"):
                prob_df = pd.DataFrame({'Catégorie': model.classes_, 'Proba': probs}).sort_values('Proba', ascending=False)
                st.bar_chart(prob_df.set_index('Catégorie'))
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("#### 🔍 Données extraites")
        # SIRET
        s_val = f"SIRET: {siret}" if siret else "SIRET: Non trouvé"
        s_color = "#059669" if siret_valid else "#DC2626"
        st.markdown(f'<div class="entity-row"><span>{s_val}</span><b style="color:{s_color}">{"✅" if siret_valid else "❌"}</b></div>', unsafe_allow_html=True)
        # IBAN
        i_val = f"IBAN: {iban[:15]}..." if iban else "IBAN: Non trouvé"
        i_color = "#059669" if iban_valid else "#DC2626"
        st.markdown(f'<div class="entity-row"><span>{i_val}</span><b style="color:{i_color}">{"✅" if iban_valid else "❌"}</b></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("#### 💬 Assistant Intelligent")
        user_q = st.text_input("Posez une question sur le document :")
        if user_q:
            with st.spinner("Analyse..."):
                answer = agent.ask(full_text, user_q)
                st.markdown(f"<div style='background:#F3F4F6; padding:15px; border-radius:10px; border-left:5px solid #0066FF;'>{answer}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        with st.expander("📄 Texte Brut (OCR)"):
            st.markdown(f'<div class="raw-text-box">{full_text[:3000]}...</div>', unsafe_allow_html=True)

    os.remove(temp_path)
else:
    st.info("Veuillez uploader un document pour démarrer l'analyse.")
    if Path("storage/models/confusion_matrix.png").exists():
        st.image("storage/models/confusion_matrix.png", caption="Performance du Cerveau DocFlow AI")