import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from semantic_engine import analyze_user
from rag_context import build_context
from genai import generate_bio, generate_learning_plan
from utils.pdf_generator import generate_pdf
import tempfile
import os

st.set_page_config(page_title="AISCA – Résultats", layout="wide")

st.title("📊 Analyse de vos Compétences")

# -------------------------
# Vérification session
# -------------------------
if "user_inputs" not in st.session_state:
    st.error("Veuillez d'abord remplir le questionnaire.")
    st.stop()

inputs = st.session_state["user_inputs"]

# -------------------------
# TEXTE UTILISATEUR POUR SBERT
# -------------------------
def build_user_text(inputs):
    text = ""
    text += " ".join([p for p in inputs["projects"] if p]) + " "
    if inputs["tech_skills"]:
        text += " ".join(inputs["tech_skills"]) + " "
    text += inputs["domain_choice"] + " "
    if inputs["soft_skills"]:
        text += " ".join(inputs["soft_skills"]) + " "
    likert_text = " ".join([f"{k} niveau {v}" for k, v in inputs["likert"].items()])
    text += likert_text + " "
    return text.lower()

user_text = build_user_text(inputs)

# -------------------------
# Analyse SBERT
# -------------------------
results = analyze_user(user_text)
block_scores = results["block_scores"]
job_reco = results["job_recommendation"]
job_scores = results["job_scores"]

st.success("Analyse terminée ✔️")

# -------------------------
# Convertir en %
# -------------------------
def to_percent_dict(d):
    return {k: int(v * 100) for k, v in d.items()}

percent_scores = to_percent_dict(block_scores)

# ==================================================================
#   VISUALISATIONS (graphiques + sauvegarde pour PDF)
# ==================================================================

# -------- DOUGHNUT (image)
def get_doughnut_figure(scores):
    labels = list(scores.keys())
    values = list(scores.values())
    colors = ["#4C8BF5", "#AA5DF5", "#F55D9A", "#F5A85D"]

    fig, ax = plt.subplots(figsize=(8, 8))

    wedges, _ = ax.pie(
        values,
        colors=colors,
        startangle=90,
        wedgeprops={'width': 0.38}
    )

    avg_score = int(sum(values) / len(values))
    ax.text(0, 0, f"{avg_score}%", ha="center", va="center", fontsize=28, color="white")

    ax.set_title("Répartition Globale des Compétences (%)", color="white", fontsize=18)
    return fig

# -------- BAR CHART (image)
def get_bar_figure(scores):
    labels = list(scores.keys())
    values = list(scores.values())

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(labels, values, color="#4C8BF5")
    ax.set_xlim(0, 100)
    for i, v in enumerate(values):
        ax.text(v + 2, i, f"{v}%", color="white", fontsize=12)

    ax.set_title("Scores par Bloc (%)", color="white")
    return fig

# -------- Affichage dans Streamlit
st.header("📊 Visualisation des Compétences")

doughnut_fig = get_doughnut_figure(percent_scores)
bar_fig = get_bar_figure(percent_scores)

col1, col2 = st.columns([1, 1])

with col1:
    st.pyplot(doughnut_fig)

with col2:
    st.pyplot(bar_fig)

# ==================================================================
#   MÉTIER RECOMMANDÉ
# ==================================================================
st.header("🏆 Métier Recommandé")

st.markdown(f"""
<div style='padding:20px; border-radius:10px; background:#1c1c1c; color:white; text-align:center; font-size:22px;'>
<b>{job_reco}</b>
</div>
""", unsafe_allow_html=True)

# ==================================================================
#   IA GÉNÉRATIVE
# ==================================================================
context = build_context(inputs, results)

st.header("🤖 Bio Professionnelle")
bio = generate_bio(context)
st.write(bio)

st.header("📘 Plan de Progression Personnalisé")
plan = generate_learning_plan(context)
st.write(plan)

# ==================================================================
#   SAUVEGARDE GRAPHIQUES POUR PDF
# ==================================================================

# Créer un dossier temporaire si besoin
os.makedirs("temp", exist_ok=True)

doughnut_path = "temp/doughnut.png"
bar_path = "temp/bar.png"

doughnut_fig.savefig(doughnut_path, dpi=200, bbox_inches="tight")
bar_fig.savefig(bar_path, dpi=200, bbox_inches="tight")

# ==================================================================
#   PDF : FORCES / FAIBLESSES
# ==================================================================

sorted_scores = sorted(percent_scores.items(), key=lambda x: x[1], reverse=True)
strengths = [f"{k} ({v}%)" for k, v in sorted_scores[:2]]
weaknesses = [f"{k} ({v}%)" for k, v in sorted_scores[-2:]]

# ==================================================================
#   BOUTON PDF
# ==================================================================
st.subheader("📄 Télécharger votre rapport professionnel")

if st.button("📥 Générer mon PDF"):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf_path = tmp.name

        generate_pdf(
            pdf_path,
            percent_scores,
            job_reco,
            bio,
            plan,
            strengths,
            weaknesses,
            doughnut_path,
            bar_path
        )

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📥 Télécharger le rapport PDF",
                data=f,
                file_name="Rapport_AISCA.pdf",
                mime="application/pdf"
            )
