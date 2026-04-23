from reportlab.pdfgen import canvas
from pathlib import Path
import random

def create_statement(filename, i):
    c = canvas.Canvas(filename)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 800, f"RELEVÉ DE COMPTE BANCAIRE N°{i+1000}")
    
    c.setFont("Helvetica", 10)
    c.drawString(50, 780, "Période : Du 01/03/2024 au 31/03/2024")
    c.drawString(50, 760, "Titulaire : M. Jean DATA")
    
    # Entête de tableau
    c.line(50, 740, 550, 740)
    c.drawString(55, 725, "Date")
    c.drawString(150, 725, "Libellé de l'opération")
    c.drawString(400, 725, "Débit")
    c.drawString(480, 725, "Crédit")
    c.line(50, 720, 550, 720)
    
    operations = ["ACHAT CB CARREFOUR", "VIR RECU SALAIRE", "PRELEV. EDF", "RETRAIT DAB PARIS"]
    y = 700
    for _ in range(10):
        c.drawString(55, y, f"{random.randint(1,31)}/03")
        c.drawString(150, y, random.choice(operations))
        if random.random() > 0.5:
            c.drawString(400, y, f"-{random.randint(10, 100)},00")
        else:
            c.drawString(480, y, f"+{random.randint(500, 2000)},00")
        y -= 20
        
    c.setFont("Helvetica-Bold", 11)
    c.drawString(300, y-20, f"SOLDE CRÉDITEUR : {random.randint(2000, 5000)},42 EUR")
    c.save()

dest = Path("data/raw/releve")
dest.mkdir(parents=True, exist_ok=True)
print("🚀 Génération de 100 relevés bancaires...")
for i in range(100):
    create_statement(str(dest / f"statement_{i}.pdf"), i)
print("✅ Fini.")