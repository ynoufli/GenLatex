import streamlit as st
import requests
from urllib.parse import quote

st.title("Génération PDF LaTeX avancée")

# --- Formulaire pour remplir les champs ---
titre = st.text_input("Titre")
introduction = st.text_area("Introduction")

# Mots-clés
motFR1 = st.text_input("Mot-clé FR 1")
motANG1 = st.text_input("Mot-clé EN 1")
motFR2 = st.text_input("Mot-clé FR 2")
motANG2 = st.text_input("Mot-clé EN 2")

# Partie 1 et Partie 2
partie1 = st.text_input("Titre Partie 1")
explications1 = st.text_area("Explications Partie 1")
partie2 = st.text_input("Titre Partie 2 (optionnel)")
explications2 = st.text_area("Explications Partie 2 (optionnel)")

# Références (toutes optionnelles)
refs = []
for i in range(1, 5):
    nom = st.text_input(f"Référence {i} - Nom auteur (optionnel)")
    titre_article = st.text_input(f"Référence {i} - Titre article (optionnel)")
    url = st.text_input(f"Référence {i} - URL (optionnel)")
    refs.append((nom, titre_article, url))

# Bouton pour générer le PDF
if st.button("Générer PDF"):

    # Template LaTeX
    template = r"""
\documentclass[a4paper,12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{hyperref}
\geometry{margin=2cm}

\title{\textbf{__Titre__}}

\begin{document}
\date{}
\maketitle

\section*{Introduction au sujet}
__Introduction__

\section*{Mots-clés}
\begin{tabular}{|p{6cm}|p{6cm}|}
\hline
\textbf{Mots-clés} & \textbf{Keywords} \\
\hline
__MotFR1__ & __MotANG1__ \\
__MotFR2__ & __MotANG2__ \\
\hline
\end{tabular}

\section*{Fondements mathématiques}

__Partie1__
__Partie2__

\section*{Plan et exploration interactive}
__exploration__

__RefsSection__

\end{document}
"""

    # Parties en gras
    partie1_latex = f"\\textbf{{1. {partie1}}}\n\n{explications1}" if partie1 and explications1 else ""
    partie2_latex = f"\n\\textbf{{2. {partie2}}}\n\n{explications2}" if partie2 and explications2 else ""

    # Références dynamiques
    refs_entries = []
    for nom, titre_article, url in refs:
        if nom and titre_article:
            url_text = f"\\url{{{url}}}" if url else ""
            refs_entries.append(f"{nom}, \\emph{{{titre_article}}} {url_text}")
    if refs_entries:
        refs_latex = "\\section*{Références}\n\\begin{enumerate}\n  \\item " + "\n  \\item ".join(refs_entries) + "\n\\end{enumerate}"
    else:
        refs_latex = ""  # Si aucune référence remplie, la section n'apparaît pas

    # Remplacer les placeholders
    latex_text = template.replace("__Titre__", titre)
    latex_text = latex_text.replace("__Introduction__", introduction)
    latex_text = latex_text.replace("__MotFR1__", motFR1)
    latex_text = latex_text.replace("__MotANG1__", motANG1)
    latex_text = latex_text.replace("__MotFR2__", motFR2)
    latex_text = latex_text.replace("__MotANG2__", motANG2)
    latex_text = latex_text.replace("__Partie1__", partie1_latex)
    latex_text = latex_text.replace("__Partie2__", partie2_latex)
    latex_text = latex_text.replace("__RefsSection__", refs_latex)
    latex_text = latex_text.replace("__exploration__", "À remplir par l'utilisateur")

    # --- Appel de l'API LaTeX ---
    encoded = quote(latex_text)
    url = f"https://latexonline.cc/compile?text={encoded}"

    response = requests.get(url)
    if response.status_code == 200:
        st.success("PDF généré avec succès !")
        st.download_button(
            label="Télécharger le PDF",
            data=response.content,
            file_name="candidature.pdf",
            mime="application/pdf"
        )
    else:
        st.error("Erreur lors de la génération du PDF")
