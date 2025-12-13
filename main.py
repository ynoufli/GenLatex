import streamlit as st
import requests
from urllib.parse import quote

st.title("Test génération PDF LaTeX")

# --- Formulaire pour remplir les champs ---
titre = st.text_input("Titre")
introduction = st.text_area("Introduction")
motFR1 = st.text_input("Mot-clé FR 1")
motANG1 = st.text_input("Mot-clé EN 1")
motFR2 = st.text_input("Mot-clé FR 2")
motANG2 = st.text_input("Mot-clé EN 2")

# Bouton pour générer le PDF
if st.button("Générer PDF"):
    # --- Template LaTeX avec placeholders ---
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

\end{document}
"""

    # --- Remplacer les placeholders ---
    latex_text = template.replace("__Titre__", titre)
    latex_text = latex_text.replace("__Introduction__", introduction)
    latex_text = latex_text.replace("__MotFR1__", motFR1)
    latex_text = latex_text.replace("__MotANG1__", motANG1)
    latex_text = latex_text.replace("__MotFR2__", motFR2)
    latex_text = latex_text.replace("__MotANG2__", motANG2)

    # --- Appel de l'API LaTeX ---
    encoded = quote(latex_text)
    url = f"https://latexonline.cc/compile?text={encoded}"

    response = requests.get(url)
    if response.status_code == 200:
        st.success("PDF généré avec succès !")
        st.download_button(
            label="Télécharger le PDF",
            data=response.content,
            file_name="test_candidature.pdf",
            mime="application/pdf"
        )
    else:
        st.error("Erreur lors de la génération du PDF")
