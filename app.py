import streamlit as st

st.set_page_config(page_title="AISCA – Accueil", layout="wide")

# ========= CSS STYLE PRO =============
st.markdown("""
<style>

.stApp {
    background-color: #1A1A1A;
}

.big-title {
    font-size: 58px;
    font-weight: 800;
    color: white;
    text-align: center;
    margin-bottom: 0px;
}

.sub-title {
    font-size: 22px;
    text-align: center;
    color: #bbbbbb;
    margin-top: -10px;
    margin-bottom: 40px;
}

.section-title {
    color: white;
    font-size: 26px;
    font-weight: 700;
    margin-top: 25px;
}

p, li {
    color: #e0e0e0 !important;
}

button[kind="secondary"] {
    background-color: #4C8BF5 !important;
    color: white !important;
    border-radius: 8px !important;
}

</style>
""", unsafe_allow_html=True)


# ========= TITRE CENTRAL ============
st.markdown("<h1 class='big-title'>🤖 AISCA – Analyse Sémantique des Compétences</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Une application IA qui analyse vos compétences et génère un rapport professionnel.</p>", unsafe_allow_html=True)

st.markdown("---")

# ========= OBJECTIFS ============
st.markdown("<div class='section-title'>🎯 Objectifs d'AISCA</div>", unsafe_allow_html=True)

st.write("""
AISCA a pour objectif de fournir une analyse complète et professionnelle de votre profil :
- Évaluer vos compétences techniques et vos soft skills  
- Identifier vos points forts et vos axes d’amélioration  
- Recommander le métier le plus adapté à votre profil  
- Générer une bio professionnelle rédigée par IA  
- Proposer un plan d’apprentissage structuré  
- Produire un rapport PDF de qualité corporate  
""")

st.markdown("---")

# ========= BOUTON CENTRÉ ============
col = st.columns(3)[1]

with col:
    go = st.button("🚀 Commencer le questionnaire", use_container_width=True)

if go:
    st.switch_page("pages/Questionnaire.py")
