# scripts/download_real_docs.py
# Version finale DocFlow AI - avec catégorie "autre" complète et robuste
import httpx
from pathlib import Path
import time

DOCS = {
    "rapport_annuel": [
        ("socgen_deu_2024.pdf", "https://usprogram.socgen.com/files/280.pdf"),
        ("amf_rapport_2023.pdf", "https://www.amf-france.org/sites/institutionnel/files/private/2024-08/amf_ra2023_bd.pdf"),
        ("credit_agricole_2024.pdf", "https://www.credit-agricole.com/pdfPreview/205573"),
        ("lvmh_rapport_2023.pdf", "https://r.lvmh-static.com/uploads/2024/03/lvmh_rapport-annuel-2023.pdf"),
        ("axa_urd_2023.pdf", "https://www-axa-com.cdn.axa-contento-118412.eu/www-axa-com/013a16d3-6b7e-4fbf-a056-593f3fd24628_axa_urd2023_accessible_va.pdf"),
    ],
    "contrat": [
        ("convention_metallurgie_2024.pdf", "https://uimm.lafabriquedelavenir.fr/wp-content/uploads/2022/02/CNN_metallurgie_consolidee-au-10-06-2024.pdf"),
        ("convention_particuliers_employeurs.pdf", "https://www.fepem.fr/wp-content/uploads/2025/03/CCN-FR-250225.pdf"),
        ("bodacc_info.json", "https://bodacc-datadila.opendatasoft.com/api/records/1.0/search/?dataset=annonces-commerciales&rows=10&sort=dateparution"),
    ],
    "releve": [
        ("axa_urd_2023.pdf", "https://www-axa-com.cdn.axa-contento-118412.eu/www-axa-com/013a16d3-6b7e-4fbf-a056-593f3fd24628_axa_urd2023_accessible_va.pdf"),
        ("sg_releve_exemple.pdf", "https://static.societegenerale.fr/pri/PRI/Repertoire_par_type_de_contenus/Fichier_a_telecharger/nouveau-releve-compte.pdf"),
    ],
    "autre": [
        # Bulletins de salaire (très utiles pour "autre")
        ("bulletin_salaire_cesu.pdf", "https://www.cesu.urssaf.fr/info/files/pdf/Modele_Bulletin_salaire.pdf"),
        ("bulletin_salaire_yvelines.pdf", "https://www.yvelines.fr/wp-content/uploads/2009/11/modele-bulletin-de-salaire.pdf"),
        ("bulletin_salaire_macsf.pdf", "https://www.macsf.fr/content/download/41489/file/Modele-bulletin-salaire-interne.pdf"),

        # Procès-verbaux et documents légaux
        ("pv_ag_sci.pdf", "https://www.indy.fr/wp-content/uploads/Modele-de-PV-dassemblee-generale-annuelle-SCI.pdf"),

        # Documents administratifs et guides officiels
        ("lexique_administratif.pdf", "https://www.modernisation.gouv.fr/files/2023-09/LexiqueAdministratif.pdf"),
        ("guide_redaction_administrative.pdf", "https://www.culture.gouv.fr/content/download/93485/file/guide_rediger-simplement_def.pdf"),

        # Certificats et attestations
        ("certificat_medical_mdp_h.pdf", "https://www.monparcourshandicap.gouv.fr/sites/default/files/2022-05/cerfa_Certificat%20m%C3%A9dical%20MDPH_15695_accessible.pdf"),
        ("attestation_honneur.pdf", "https://immatriculation.ants.gouv.fr/files/0e166cbb-ea9e-4cf2-8b99-c3df1801b6c7/attestation-sur-l-honneur.pdf"),
    ],
}

# Fallbacks pour les URLs fragiles
FALLBACK_URLS = {
    "socgen_deu_2024.pdf": ["https://www.societegenerale.com/sites/default/files/documents/2024-03/societe-generale-deu-2024.pdf"],
    "amf_rapport_2023.pdf": ["https://www.vie-publique.fr/sites/default/files/rapport/pdf/294417.pdf"],
}

BASE = Path("data/raw")

def download(name: str, url: str, folder: str, retry_count: int = 0) -> bool:
    dest = BASE / folder / name
    if dest.exists():
        print(f"  ✅ Déjà présent : {name}")
        return True

    print(f"  📥 Téléchargement : {name}...")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            "Accept": "application/pdf,application/json,*/*",
            "Accept-Language": "fr-FR,fr;q=0.9",
        }

        with httpx.Client(timeout=180, follow_redirects=True, headers=headers) as client:
            r = client.get(url)
            r.raise_for_status()

            content = r.content
            content_type = r.headers.get("content-type", "").lower()

            if len(content) < 2000:
                print(f"  ⚠️ Trop petit ({len(content)} bytes) → probablement erreur")
                return False

            if name.lower().endswith(".pdf") and not content.startswith(b'%PDF-'):
                if "html" in content_type or b"<html" in content[:500]:
                    print(f"  ⚠️ HTML au lieu de PDF")
                    return False

            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(content)
            size_kb = len(content) / 1024
            print(f"  ✅ OK — {size_kb:.0f} KB")
            return True

    except Exception as e:
        print(f"  ❌ Erreur : {type(e).__name__} - {e}")

    return False


def download_with_fallback(name: str, url: str, folder: str) -> bool:
    if download(name, url, folder):
        return True

    if name in FALLBACK_URLS:
        print(f"  🔄 Tentative fallbacks...")
        for fb in FALLBACK_URLS[name]:
            time.sleep(1.5)
            if download(name, fb, folder):
                return True
    return False


def main():
    print("=" * 70)
    print("🚀 Téléchargement documents DocFlow AI (catégorie 'autre' complète)")
    print("=" * 70)

    success = 0
    fail = 0

    for folder, files in DOCS.items():
        print(f"\n📁 --- {folder.upper()} ---")
        for name, url in files:
            if download_with_fallback(name, url, folder):
                success += 1
            else:
                fail += 1
            time.sleep(0.8)

    print("\n" + "=" * 70)
    print(f"✅ {success} réussis | {fail} échecs")
    print("=" * 70)

    if success > 0:
        print(f"\n📂 Sauvegardés dans : {BASE.absolute()}")
        for folder in DOCS:
            p = BASE / folder
            if p.exists():
                fs = sorted(p.glob("*"))
                if fs:
                    print(f"  📂 {folder}/ ({len(fs)} fichiers)")
                    for f in fs:
                        print(f"     • {f.name} ({f.stat().st_size / 1024:.0f} KB)")

if __name__ == "__main__":
    main()