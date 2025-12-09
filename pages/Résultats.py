import streamlit as st
from semantic_engine import analyze_user
from rag_context import build_context
from genai import generate_bio, generate_learning_plan

st.set_page_config(page_title="AISCA – Résultats", layout="wide")

st.title("📊 Résultats de votre analyse")

# ----------------------------------------
# Vérification session
# ----------------------------------------
if "user_inputs" not in st.session_state:
    st.error("Veuillez d'abord remplir le questionnaire.")
    st.stop()

inputs = st.session_state["user_inputs"]

# ----------------------------------------
# Fonction : convertir dict → texte brut (compatible SBERT)
# ----------------------------------------
def build_user_text(inputs):
    text = ""

    # Projets
    text += " ".join([p for p in inputs["projects"] if p]) + " "

    # Compétences techniques
    if inputs["tech_skills"]:
        text += " ".join(inputs["tech_skills"]) + " "

    # Domaine préféré
    text += inputs["domain_choice"] + " "

    # Soft skills
    if inputs["soft_skills"]:
        text += " ".join(inputs["soft_skills"]) + " "

    # Notes Likert
    likert_text = " ".join([f"{k} niveau {v}" for k, v in inputs["likert"].items()])
    text += likert_text + " "

    # Informations supplémentaires
    text += f"Experience: {inputs['experience']} "
    text += f"Education: {inputs['education']} "
    if inputs["certified"]:
        text += "certified "

    return text.lower()


# ----------------------------------------
# Préparer le texte utilisateur
# ----------------------------------------
user_text = build_user_text(inputs)

# ----------------------------------------
# Analyse backend SBERT
# ----------------------------------------
results = analyze_user(user_text)

st.success("Analyse SBERT terminée ✔️")

# ----------------------------------------
# Affichage scores par bloc
# ----------------------------------------
st.subheader("📈 Scores par bloc")
st.write(results["block_scores"])

# ----------------------------------------
# Scores par métier
# ----------------------------------------
st.subheader("💼 Scores des métiers")
st.write(results["job_scores"])

# ----------------------------------------
# Meilleur métier recommandé
# ----------------------------------------
st.subheader("🏆 Métier recommandé")
st.write(f"✔ {results['job_recommendation']}")

# ----------------------------------------
# Contexte génératif (RAG)
# ----------------------------------------
context = build_context(results)

with st.expander("🧠 Afficher le contexte utilisé pour l’IA"):
    st.text(context)

# ----------------------------------------
# IA Générative : Bio
# ----------------------------------------
st.subheader("🤖 Bio générée")
bio = generate_bio(context)
st.write(bio)

# ----------------------------------------
# IA Générative : Plan
# ----------------------------------------
st.subheader("📘 Plan de progression")
plan = generate_learning_plan(context)
st.write(plan)
