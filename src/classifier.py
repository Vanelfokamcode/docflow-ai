# src/classifier.py
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import os

def train_model(csv_path="data/dataset.csv", model_path="storage/model.joblib"):
    if not os.path.exists(csv_path):
        print(f"Erreur : Le fichier {csv_path} n'existe pas. Lance d'abord scripts/prepare_ml_data.py")
        return

    # 1. Charger les données
    df = pd.read_csv(csv_path)
    
    # 2. Séparer Entraînement / Test (80% / 20%)
    # Correction ici : test_size et pas test_test_size
    X_train, X_test, y_train, y_test = train_test_split(
        df['text'], df['label'], test_size=0.2, random_state=42
    )
    
    # 3. Créer le Pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000)),
        ('clf', LogisticRegression(class_weight='balanced'))
    ])
    
    # 4. Entraînement
    print(f"Entraînement sur {len(X_train)} pages...")
    pipeline.fit(X_train, y_train)
    
    # 5. Évaluation
    y_pred = pipeline.predict(X_test)
    print("\n--- RAPPORT DE PERFORMANCE ---")
    print(classification_report(y_test, y_pred))
    
    # 6. Sauvegarde
    os.makedirs("storage", exist_ok=True)
    joblib.dump(pipeline, model_path)
    print(f"✅ Modèle sauvegardé dans {model_path}")

if __name__ == "__main__":
    train_model()