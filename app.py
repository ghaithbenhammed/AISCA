import streamlit as st

st.set_page_config(page_title="AISCA", layout="wide")

st.title("AISCA - Analyse Sémantique des Compétences")

st.subheader("Questionnaire Utilisateur")

# Exemple de question texte
projet = st.text_area("Décrivez un projet que vous avez réalisé")

# Exemple de valeur Likert
python_level = st.slider("Votre niveau en Python", 1, 5, 3)

# Bouton analyser
if st.button("Analyser mon profil"):
    st.write("⏳ En attente des résultats (backend)...")
