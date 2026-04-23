# 1. Image de base Python
FROM python:3.12-slim

# 2. Installation des dépendances système (Tesseract pour l'OCR)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-fra \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# 3. Dossier de travail
WORKDIR /app

# 4. Copie des fichiers de dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copie du code source
COPY src/ ./src/
COPY storage/ ./storage/
COPY app.py .

# 6. Exposition du port Streamlit
EXPOSE 8501

# 7. Commande de lancement
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]