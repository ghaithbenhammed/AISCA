import streamlit as st
from semantic_engine import analyze_user
from rag_context import build_context
from genai import generate_bio, generate_learning_plan

st.set_page_config(page_title="AISCA – Résultats", layout="wide")

st.title("📊 Résultats de votre analyse")

# --- Récupération des réponses ---
if "user_inputs" not in st.session_state:
    st.error("Veuillez d'abord remplir le questionnaire.")
    st.stop()

inputs = st.session_state["user_inputs"]

# --- Analyse backend ---
results = analyze_user(inputs)

st.success("Analyse SBERT terminée ✔️")

# --- Affichage scores ---
st.subheader("📈 Scores par bloc")
st.write(results["block_scores"])

# --- Build contexte ---
context = build_context(results)

with st.expander("Afficher le contexte utilisé pour l’IA"):
    st.text(context)

# --- IA Générative ---
st.subheader("🤖 Bio générée")
st.write(generate_bio(context))

st.subheader("📘 Plan de progression")
st.write(generate_learning_plan(context))

# --- Recommandations métiers ---
st.subheader("💼 Métiers recommandés")
for job in results["job_recommendations"]:
    st.write("✔", job)
