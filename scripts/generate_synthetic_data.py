"""
Générateur de factures synthétiques

Ce script crée des PDFs de factures réalistes pour permettre
au modèle de Machine Learning d'avoir plusieurs classes.
"""

from reportlab.pdfgen import canvas
from pathlib import Path
import random
import os

def create_invoice(filename, invoice_num):
    c = canvas.Canvas(filename)
    
    # On simule une structure de facture
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, f"FACTURE N° {invoice_num}")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, 780, f"Date: {random.randint(1,28)}/03/2024")
    
    # On insère un SIRET valide pour l'entraînement
    c.drawString(50, 760, "SIRET: 77567041700010") # SIRET LVMH pour le test
    
    c.drawString(50, 700, "Description")
    c.drawString(400, 700, "Montant")
    c.line(50, 695, 550, 695)
    
    ht = random.randint(100, 5000)
    tva = ht * 0.20
    ttc = ht + tva
    
    c.drawString(50, 670, "Prestation de service IT")
    c.drawString(400, 670, f"{ht:.2f} EUR")
    
    c.drawString(300, 600, "Total HT:")
    c.drawString(400, 600, f"{ht:.2f} EUR")
    
    c.drawString(300, 580, "TVA (20%):")
    c.drawString(400, 580, f"{tva:.2f} EUR")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(300, 550, "TOTAL TTC:")
    c.drawString(400, 550, f"{ttc:.2f} EUR")
    
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 100, "Merci de régler cette facture sous 30 jours.")
    c.drawString(50, 85, "IBAN: FR76 1234 5678 9012 3456 7890 185")
    
    c.save()

def generate_batch(count=50):
    output_dir = Path("data/raw/facture")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Génération de {count} factures synthétiques...")
    for i in range(count):
        file_path = output_dir / f"facture_synth_{i:03d}.pdf"
        create_invoice(str(file_path), f"2024-{i:03d}")

if __name__ == "__main__":
    generate_batch()