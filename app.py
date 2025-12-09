import streamlit as st

st.set_page_config(page_title="AISCA – Accueil", layout="wide")

# --- Style minimaliste ---
st.markdown("""
<style>

    .big-title-container {
        width: 100%;
        display: flex;
        justify-content: center;
        margin-top: 10px;
        margin-bottom: 0px;
    }

    .big-title {
        font-size: 60px;        /* énorme */
        font-weight: 800;       /* très pro */
        color: white;           
        text-align: center;
    }

    .sub-title {
        font-size: 22px;
        text-align: center;
        color: #cccccc;
        margin-bottom: 40px;
    }

    .stApp {
        background-color: #1a1a1a;
    }
</style>
""", unsafe_allow_html=True)

# --- Titre ---
st.markdown("""
<div class="big-title-container">
    <h1 class="big-title">🤖 AISCA – Analyse Sémantique des Compétences</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("<p class='sub-title'>Une application IA qui analyse vos compétences et recommande des métiers adaptés.</p>", unsafe_allow_html=True)

st.markdown("---")

# --- Présentation ---
st.markdown("### 🎯 Objectifs d'AISCA")
st.write("""
- Identifier vos compétences fortes et vos axes d'amélioration  
- Générer une analyse IA personnalisée  
- Recommander des métiers adaptés à votre profil  
- Fournir un plan d'apprentissage basé sur vos réponses  
""")

st.markdown("---")

# --- Bouton centré ---
center = st.columns(3)[1]
with center:
    start = st.button("🚀 Commencer le questionnaire", use_container_width=True)

if start:
    st.switch_page("pages/Questionnaire.py")
