from reportlab.pdfgen import canvas
from pathlib import Path
import random

def create_contract(filename, i):
    c = canvas.Canvas(filename)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 800, f"CONTRAT DE PRESTATION DE SERVICE - Réf: {2024+i}")
    c.setFont("Helvetica", 10)
    text = [
        "ENTRE : La société TECH-INNOV, ci-après dénommée 'Le Prestataire'",
        "ET : L'entreprise CLIENT-DE-TEST, ci-après dénommée 'Le Client'",
        "",
        "ARTICLE 1 - OBJET",
        "Le présent contrat définit les conditions techniques de la mission.",
        "ARTICLE 2 - DURÉE ET RÉSILIATION",
        "Le contrat est conclu pour une durée de 12 mois renouvelable.",
        "ARTICLE 3 - CONFIDENTIALITÉ ET RGPD",
        "Les parties s'engagent à ne pas divulguer les données sensibles.",
        "Fait à Paris, le 23/04/2026."
    ]
    y = 750
    for line in text:
        c.drawString(50, y, line)
        y -= 20
    c.save()

dest = Path("data/raw/contrat")
dest.mkdir(parents=True, exist_ok=True)
print("🚀 Génération de 100 contrats...")
for i in range(100):
    create_contract(str(dest / f"contract_synth_{i}.pdf"), i)
print("✅ Terminé.")