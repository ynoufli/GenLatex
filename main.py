import streamlit as st
import requests
from urllib.parse import quote

st.info("Veuillez remplir obligatoirement les champs notés avec * afin de générer votre candidature.")
#st.set_page_config(page_title="Génération de candidature", layout="centered")
st.title("Génération de candidature (PDF LaTeX)")

# --------------------
# FORMULAIRE
# --------------------
titre = st.text_input("Titre du sujet *")
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
partie1 = st.text_input("Titre de la partie 1 *")
explications1 = st.text_area("Explications Partie 1 *")

partie2 = st.text_input("Titre de la partie 2 (optionnel)")
explications2 = st.text_area("Explications Partie 2 (optionnel)")

st.subheader("Plan et exploration interactive")
exploration = st.text_area("Description du plan *")

st.subheader("Références")
refs = []
for i in range(4):
    nom = st.text_input(f"Auteur {i+1} *")
    titre_ref = st.text_input(f"Titre de l'article {i+1} *")
    url_ref = st.text_input(f"URL {i+1} (optionnel)")
    if nom and titre_ref:
        refs.append((nom, titre_ref, url_ref))

# --------------------
# BOUTON
# --------------------
if st.button("Générer le PDF"):
    if not all([titre, introduction, partie1, explications1, exploration]) or len(motcles) < 2 or len(refs) < 1:
        st.error("Veuillez remplir tous les champs obligatoires, au moins 2 mots-clés et 1 référence.")
    else:
        # -------- Mots-clés --------
        mots_latex = ""
        for fr, en in motcles:
            mots_latex += f"{fr} & {en} \\\\\n"

        # -------- Partie 2 --------
        partie2_latex = ""
        if partie2 and explications2:
            partie2_latex = f"""
2. {partie2}

{explications2}
"""

        # -------- Partie 1 numérotée --------
        partie1_latex = f"1. {partie1}\n\n{explications1}"

        # -------- Références --------
        refs_latex = ""
        for nom, titre_ref, url_ref in refs:
            url_latex = f"\\url{{{url_ref}}}" if url_ref else ""
            refs_latex += f"\\item {nom}, \\emph{{{titre_ref}}}. {url_latex}\n"

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
{partie1_latex}

{partie2_latex}

\\section*{{Plan et exploration interactive}}
{exploration}

\\section*{{Références}}
\\begin{{enumerate}}
{refs_latex}
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
