import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time
import os
import tempfile

from semantic_engine import analyze_user
from rag_context import build_context
from genai import generate_bio, generate_learning_plan
from utils.pdf_generator import generate_pdf

st.set_page_config(page_title="AISCA – Résultats", layout="wide")

# ============================================================
# 🔥 CSS — Animation loader
# ============================================================
st.markdown("""
<style>
.loader-bar {
  width: 260px;
  height: 6px;
  background: #333;
  border-radius: 10px;
  overflow: hidden;
  margin-top: 8px;
}
.loader-bar::before {
  content: "";
  width: 40%;
  height: 100%;
  background: linear-gradient(90deg, #4C8BF5, #AA5DF5);
  display: block;
  animation: slide 1.2s infinite;
}
@keyframes slide {
  0%   { transform: translateX(-40%); }
  100% { transform: translateX(140%); }
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# 🔍 Vérification des données
# ============================================================
inputs = st.session_state.get("user_inputs")
if inputs is None:
    st.error("Veuillez d'abord remplir le questionnaire.")
    st.stop()

# ============================================================
# 🟦 Titre — affiché immédiatement !
# ============================================================
st.markdown("<h1>📊 Analyse de vos Compétences</h1>", unsafe_allow_html=True)

# ============================================================
# 🧪 Placeholder de l’animation (affiché DIRECTEMENT)
# ============================================================
sbert_placeholder = st.empty()

sbert_placeholder.markdown("""
### 🔍 Analyse sémantique SBERT en cours...
<div class="loader-bar"></div>
""", unsafe_allow_html=True)

# ============================================================
# 🧠 Construction du texte pour SBERT
# ============================================================
def build_user_text(inputs):
    text = " ".join([p for p in inputs["projects"] if p.strip()])
    text += " " + " ".join(inputs["tech_skills"])
    text += " " + inputs["domain_choice"]
    text += " " + " ".join(inputs["soft_skills"])
    return text.lower()

user_text = build_user_text(inputs)

# ============================================================
# 🔥 Analyse SBERT — (pendant que l’animation s’affiche)
# ============================================================
if "results_sbert" not in st.session_state:
    st.session_state["results_sbert"] = analyze_user(user_text)

results = st.session_state["results_sbert"]
percent_scores = {k: int(v * 100) for k, v in results["block_scores"].items()}
job_reco = results["job_recommendation"]

# ➜ On efface l’animation après analyse
time.sleep(0.5)
sbert_placeholder.empty()

# ============================================================
# 📈 VISUALISATIONS — Elles apparaissent APRES l’analyse
# ============================================================
def plot_doughnut(scores):
    labels = list(scores.keys())
    values = list(scores.values())
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.55, textinfo="label+percent",
        marker=dict(colors=["#4C8BF5", "#AA5DF5", "#F55D9A", "#F5A85D"])
    ))
    fig.update_layout(title="Répartition des Compétences (%)", title_x=0.5,
                      paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
    return fig

def plot_bar(scores):
    fig = go.Figure(go.Bar(
        x=list(scores.values()), y=list(scores.keys()),
        orientation="h", marker_color="#4C8BF5"
    ))
    fig.update_layout(
        title="Scores par Bloc (%)", title_x=0.5,
        xaxis=dict(range=[0, 100]),
        paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
    return fig

st.header("📊 Visualisation des Compétences")
col1, col2 = st.columns(2)

doughnut_fig = plot_doughnut(percent_scores)
bar_fig = plot_bar(percent_scores)

with col1:
    st.plotly_chart(doughnut_fig, use_container_width=True)
with col2:
    st.plotly_chart(bar_fig, use_container_width=True)

# ============================================================
# 🤖 IA Générative — avec loader individuel
# ============================================================
st.header("🤖 Analyse IA Générative")

context = build_context(inputs, results)

bio_placeholder = st.empty()
plan_placeholder = st.empty()

# --- Bio ---
if "bio_text" not in st.session_state:
    bio_placeholder.markdown("""
    ### 🧠 Génération de la bio professionnelle...
    <div class="loader-bar"></div>
    """, unsafe_allow_html=True)
    st.session_state["bio_text"] = generate_bio(context)
    time.sleep(0.5)
    bio_placeholder.empty()

# --- Plan ---
if "plan_text" not in st.session_state:
    plan_placeholder.markdown("""
    ### 📘 Génération du plan d’apprentissage...
    <div class="loader-bar"></div>
    """, unsafe_allow_html=True)
    st.session_state["plan_text"] = generate_learning_plan(context)
    time.sleep(0.5)
    plan_placeholder.empty()

bio = st.session_state["bio_text"]
plan = st.session_state["plan_text"]

st.subheader("📌 Bio Professionnelle Générée")
st.write(bio)

st.subheader("📘 Plan d'Apprentissage Personnalisé")
st.write(plan)

# ============================================================
# 📄 Export PDF – direct
# ============================================================
st.header("📄 Télécharger votre rapport PDF")

os.makedirs("temp", exist_ok=True)
doughnut_path = "temp/doughnut.png"
bar_path = "temp/bar.png"

try:
    doughnut_fig.update_layout(paper_bgcolor="white", font=dict(color="black")).write_image(doughnut_path)
    bar_fig.update_layout(paper_bgcolor="white", font=dict(color="black")).write_image(bar_path)
except:
    doughnut_path = None
    bar_path = None

with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
    pdf_path = tmp.name
    generate_pdf(pdf_path, percent_scores, job_reco, bio, plan, doughnut_path, bar_path)

    st.download_button(
        label="📥 Télécharger le Rapport AISCA",
        data=open(pdf_path, "rb").read(),
        file_name="Rapport_AISCA.pdf",
        mime="application/pdf",
        use_container_width=True
    )
