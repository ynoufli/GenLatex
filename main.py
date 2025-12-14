import streamlit as st
import requests
from urllib.parse import quote

st.set_page_config(page_title="Génération PDF LaTeX", layout="centered")
st.title("Génération de candidature (PDF LaTeX)")

# --------------------
# FORMULAIRE
# --------------------
titre = st.text_input("Titre du projet *")
introduction = st.text_area("Introduction *")

st.subheader("Mots-clés")
motcles = []
for i in range(5):
    col1, col2 = st.columns(2)
    fr = col1.text_input(f"Mot FR {i+1}")
    en = col2.text_input(f"Mot EN {i+1}")
    if fr and en:
        motcles.append((fr, en))

st.subheader("Fondements mathématiques")
partie1 = st.text_input("Titre Partie 1 *")
explications1 = st.text_area("Explications Partie 1 *")

partie2 = st.text_input("Titre Partie 2 (optionnel)")
explications2 = st.text_area("Explications Partie 2 (optionnel)")

st.subheader("Plan et exploration interactive")
exploration = st.text_area("Description du plan *")

st.subheader("Référence principale")
nom_ref = st.text_input("Auteur *")
titre_ref = st.text_input("Titre de l'article *")
url_ref = st.text_input("URL (optionnel)")

# --------------------
# BOUTON
# --------------------
if st.button("Générer le PDF"):
    if not all([titre, introduction, partie1, explications1, exploration, nom_ref, titre_ref]) or len(motcles) < 2:
        st.error("Veuillez remplir tous les champs obligatoires (et au moins 2 mots-clés).")
    else:
        # -------- Mots-clés --------
        mots_latex = ""
        for fr, en in motcles:
            mots_latex += f"{fr} & {en} \\\\\n"

        # -------- Partie 2 --------
        partie2_latex = ""
        if partie2 and explications2:
            partie2_latex = f"""
\\subsection*{{{partie2}}}

{explications2}
"""

        # -------- URL référence --------
        url_latex = f"\\url{{{url_ref}}}" if url_ref else ""

        # -------- TEMPLATE FINAL --------
        latex = f"""
\\documentclass[a4paper,12pt]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{geometry}}
\\usepackage[colorlinks=true, linkcolor=blue, urlcolor=blue]{{hyperref}}
\\geometry{{margin=2cm}}

\\title{{\\textbf{{{titre}}}}}

\\begin{{document}}
\\date{{}}
\\maketitle

\\section*{{Introduction au sujet}}
{introduction}

\\section*{{Mots-clés}}
\\begin{{tabular}}{{|p{{6cm}}|p{{6cm}}|}}
\\hline
\\textbf{{Mots-clés}} & \\textbf{{Keywords}} \\\\
\\hline
{mots_latex}
\\hline
\\end{{tabular}}

\\section*{{Fondements mathématiques}}

\\subsection*{{{partie1}}}
{explications1}

{partie2_latex}

\\section*{{Plan et exploration interactive}}
{exploration}

\\section*{{Références}}
\\begin{{enumerate}}
\\item {nom_ref}, \\emph{{{titre_ref}}}. {url_latex}
\\item Acerola, \\emph{{Realistic Ocean Simulation with FFT}}. \\url{{https://www.youtube.com/@Acerola_t}}
\\end{{enumerate}}

\\end{{document}}
"""

        encoded = quote(latex)
        url = f"https://latexonline.cc/compile?text={encoded}"
        response = requests.get(url)

        if response.status_code == 200:
            st.success("PDF généré avec succès")
            st.download_button(
                "Télécharger le PDF",
                response.content,
                file_name="candidature.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Erreur lors de la génération du PDF")
