"""
Step 6 — AI Agent (Ollama)

Cet agent utilise un LLM local pour analyser le texte extrait
et répondre à des questions complexes en langage naturel.
"""

import requests
import json

class DocAgent:
    def __init__(self, model="qwen2.5:1.5b"): # On change pour 1.5b
        self.model = model
        self.api_url = "http://localhost:11434/api/generate"

    def ask(self, context, question):
        prompt = f"""
        [ROLE] Analyste financier.
        [CONTEXTE] {context[:1500]} # On réduit un peu à 1500 chars
        [QUESTION] {question}
        [REPONSE COURTE EN FRANÇAIS]
        """
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 100, # On limite la réponse à ~75 mots pour aller vite
                "temperature": 0    # 0 = réponse déterministe, plus rapide
            }
        }
        
        try:
            # Timeout à 180 secondes
            response = requests.post(self.api_url, json=payload, timeout=180)
            response.raise_for_status()
            return response.json().get('response', "Pas de réponse.")
        except Exception as e:
            return f"⚠️ Timeout ou erreur : {e}"