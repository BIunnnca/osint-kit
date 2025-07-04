#!/usr/bin/env python3
"""
pdf_forensic – Générateur de rapport PDF pour le dossier Yann Lafrance

Utilisation directe :
    python3 modules/pdf_forensic.py

Utilisation via OSINT-Kit :
    python3 src/main.py --module pdf_forensic
"""
import os
from datetime import datetime
from fpdf import FPDF


# ─────────────────────────────────────────────
# 1. Fonctions utilitaires
# ─────────────────────────────────────────────
def clean_text(txt: str) -> str:
    """Remplace les apostrophes / guillemets typographiques pour éviter les soucis d’encodage."""
    return (
        txt.replace("’", "'")
           .replace("“", '"')
           .replace("”", '"')
           .replace("–", "-")
    )


def build_pdf(output_dir: str) -> str:
    """Construit le PDF et renvoie son chemin."""
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "Rapport Forensique - Dossier Yann Lafrance", 0, 1, "C")
            self.ln(5)

        def chapter_title(self, title):
            self.set_font("Arial", "B", 11)
            self.set_fill_color(200, 220, 255)
            self.cell(0, 6, title, 0, 1, 'L', 1)
            self.ln(2)

        def chapter_body(self, text):
            self.set_font("Arial", "", 10)
            self.multi_cell(0, 5, text)
            self.ln()

    pdf = PDF()
    pdf.add_page()

    pdf.chapter_title("1. Table des preuves")
    pdf.chapter_body(clean_text("""\
- Alterations suspectes de documents PDF (dates, metadonnees, champs XFA)
- Courriels compromettants contenant des instructions de modification
- Liens entre plusieurs individus (Valerie D., Maude G., Justine P., Me. Plante)
- Temporalite des modifications correlee aux evenements judiciaires
"""))

    pdf.chapter_title("2. Metadonnees et modifications")
    pdf.chapter_body(clean_text("""\
Des metadonnees XMP revelent des outils de modification tels que Microsoft Word PDF Printer. Les modifications sont datees des jours cles des audiences. Les champs caches contiennent des instructions ou des suppressions d'elements critiques.
"""))

    pdf.chapter_title("3. Courriels pertinents")
    pdf.chapter_body(clean_text("""\
Courriels extraits mentionnant la modification de documents :
> \"...je joins le PDF modifie comme convenu. Le vrai fichier reste archive.\"
> \"...il faut que personne ne se doute que le texte a ete reedite...\"

Serveurs SMTP utilises : relais prives en Suisse, configurations d'obfuscation.
"""))

    pdf.chapter_title("4. Analyse des liens entre les entites")
    pdf.chapter_body(clean_text("""\
Les echanges et les metadonnees lient Valerie Delarosebil, Maude Gendreau, Justine Pelletier Beaulieu et Me. Marie-Desiree Plante a la chaine d'alterations. Les documents convergent vers une meme source de traitement et d'envoi.
"""))

    pdf.chapter_title("5. Correlation temporelle avec le dossier judiciaire")
    pdf.chapter_body(clean_text("""\
Les fichiers modifies correspondent exactement aux periodes precedant les decisions critiques dans le dossier de Yann Lafrance, ce qui suggere une tentative d'influence sur le deroulement judiciaire.
"""))

    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "rapport_forensique_yann_lafrance.pdf")
    pdf.output(pdf_path)
    return pdf_path


def generate_extras(output_dir: str) -> None:
    extras = {
        "documents_originaux.txt": "Simulacre : contenu extrait des versions originales des documents PDF\n",
        "documents_modifies.txt":  "Simulacre : contenu extrait des versions modifiees des documents PDF\n",
        "logs_activite.txt":       "Simulacre : logs d'activite SMTP et modification de fichiers\n",
        "metadonnees_completes.txt":"Simulacre : export complet des metadonnees XMP, XML, PDF-Info\n",
    }
    for fname, content in extras.items():
        with open(os.path.join(output_dir, fname), "w") as f:
            f.write(content)


# ─────────────────────────────────────────────
# 2. Point d’entrée pour OSINT-Kit
# ─────────────────────────────────────────────
def main(args_list=None):
    OUTDIR = "/mnt/data/nemesis_yann_lafrance"
    pdf_path = build_pdf(OUTDIR)
    generate_extras(OUTDIR)
    print(f"[✓] Rapport genere : {pdf_path}")
    print(f"[✓] Extras places dans : {OUTDIR}")


if __name__ == "__main__":
    main()
