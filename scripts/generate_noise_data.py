from reportlab.pdfgen import canvas
from pathlib import Path
import random

def create_noise_pdf(filename, i):
    c = canvas.Canvas(filename)
    c.setFont("Helvetica", 10)
    
    # Sujets aléatoires pour varier le vocabulaire
    subjects = [
        "Note de service concernant la machine à café",
        "Compte-rendu de la réunion d'équipe du mardi",
        "Candidature pour le poste de Data Engineer",
        "Demande de congés payés pour la période estivale",
        "Guide d'utilisation de l'imprimante du 3ème étage"
    ]
    
    c.drawString(50, 800, random.choice(subjects))
    
    # Génération de texte "administratif" aléatoire
    text = [
        "Madame, Monsieur,",
        f"Suite à notre entretien du {random.randint(1,28)}/04, je vous informe que...",
        "Le projet avance conformément au planning initial.",
        "Veuillez trouver ci-joint les documents demandés par la direction.",
        "Cordialement, L'équipe administrative."
    ]
    
    y = 750
    for line in text:
        c.drawString(50, y, line)
        y -= 20
    c.save()

dest = Path("data/raw/autre")
dest.mkdir(parents=True, exist_ok=True)
print("🚀 Génération de 150 documents 'autre'...")
for i in range(150):
    create_noise_pdf(str(dest / f"noise_{i}.pdf"), i)
print("✅ Fini.")