import streamlit as st
import plotly.graph_objects as go
import numpy as np
import tempfile
import os
import time

from semantic_engine import analyze_user
from rag_context import build_context
from genai import generate_bio, generate_learning_plan
from utils.pdf_generator import generate_pdf

st.set_page_config(
    page_title="AISCA - Résultats",
    layout="wide"
)

# ==========================================================
# STYLE
# ==========================================================

st.markdown("""
<style>

.loader-bar{
width:260px;
height:6px;
background:#303030;
border-radius:10px;
overflow:hidden;
margin-top:8px;
}

.loader-bar::before{
content:"";
display:block;
height:100%;
width:40%;
background:linear-gradient(90deg,#4C8BF5,#AA5DF5);
animation:slide 1.1s infinite;
}

@keyframes slide{
0%{transform:translateX(-40%);}
100%{transform:translateX(160%);}
}

.metric-card{

background:#202020;

padding:20px;

border-radius:12px;

border:1px solid #333;

text-align:center;

}

.metric-value{

font-size:38px;

font-weight:bold;

color:#4C8BF5;

}

.metric-title{

font-size:18px;

color:white;

}

.small-title{

font-size:24px;

font-weight:bold;

margin-top:20px;

}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# VERIFICATION
# ==========================================================

inputs = st.session_state.get("user_inputs")

if inputs is None:

    st.error("Veuillez remplir le questionnaire.")

    st.stop()

# ==========================================================
# TITRE
# ==========================================================

st.markdown("# 📊 Analyse de vos Compétences")

# ==========================================================
# CONSTRUCTION PROFIL TEXTE
# ==========================================================

def build_user_text(inputs):

    text = []

    # Domaine
    text.append(
        f"Le candidat souhaite travailler dans le domaine {inputs['domain_choice']}."
    )

    # Niveau
    text.append(
        f"Niveau d'étude : {inputs['education']}."
    )

    # Expérience
    text.append(
        f"Expérience professionnelle : {inputs['experience']}."
    )

    # Certifications
    if inputs["certifications"]:

        if "Aucune" not in inputs["certifications"]:

            certifs = ", ".join(inputs["certifications"])

            text.append(
                f"Le candidat possède les certifications suivantes : {certifs}."
            )

        else:

            text.append(
                "Le candidat ne possède pas encore de certification professionnelle."
            )

    # Compétences techniques
    if inputs["tech_skills"]:

        text.append(
            "Compétences techniques : "
            + ", ".join(inputs["tech_skills"])
        )

    # Frameworks (si tu les as ajoutés dans le questionnaire)
    if "frameworks" in inputs and inputs["frameworks"]:

        text.append(
            "Frameworks utilisés : "
            + ", ".join(inputs["frameworks"])
        )

    # Types de projets
    if "project_types" in inputs and inputs["project_types"]:

        text.append(
            "Types de projets réalisés : "
            + ", ".join(inputs["project_types"])
        )

    # Soft skills
    if inputs["soft_skills"]:

        text.append(
            "Soft skills : "
            + ", ".join(inputs["soft_skills"])
        )

    # Langues
    if "languages" in inputs and inputs["languages"]:

        text.append(
            "Langues : "
            + ", ".join(inputs["languages"])
        )

    # Objectif professionnel
    if "career_goal" in inputs:

        text.append(
            f"Objectif professionnel : {inputs['career_goal']}."
        )

    # Auto-évaluation
    text.append(f"""
Python : {inputs['likert']['python']}/5
Machine Learning : {inputs['likert']['ml']}/5
Statistiques : {inputs['likert']['stats']}/5
Visualisation : {inputs['likert']['viz']}/5
NLP : {inputs['likert']['nlp']}/5
Cloud : {inputs['likert']['cloud']}/5
""")

    # Projets
    for projet in inputs["projects"]:

        if projet.strip():

            text.append(projet)

    return "\n".join(text).lower()


user_text = build_user_text(inputs)

# ==========================================================
# ANALYSE SBERT
# ==========================================================

loader=st.empty()

loader.markdown("""

### 🔍 Analyse sémantique SBERT...

<div class="loader-bar"></div>

""",unsafe_allow_html=True)

if "results_sbert" not in st.session_state:

    st.session_state["results_sbert"]=analyze_user(user_text)

results=st.session_state["results_sbert"]

time.sleep(0.4)

loader.empty()

# ==========================================================
# EXTRACTION DES RESULTATS
# ==========================================================

block_scores=results["block_scores"]

job_scores=results["job_scores"]

job_reco=results["job_recommendation"]

matched_competencies=results["matched_competencies"]

matched_micro_skills=results["matched_micro_skills"]

strengths=results["strengths"]

weaknesses=results["weaknesses"]

job_details=results["job_details"]

percent_scores={

k:int(v*100)

for k,v in block_scores.items()

}

global_score=int(

np.mean(

list(percent_scores.values())

)

)

top_jobs=sorted(

job_scores.items(),

key=lambda x:x[1],

reverse=True

)

# ==========================================================
# KPI PRINCIPAUX
# ==========================================================

col1,col2,col3=st.columns(3)

with col1:

    st.metric(

        "🎯 Score Global",

        f"{global_score}%"

    )

with col2:

    st.metric(

        "💼 Métier recommandé",

        job_reco

    )

with col3:

    st.metric(

        "📚 Compétences détectées",

        sum(

            len(v)

            for v in matched_competencies.values()

        )

    )
# ==========================================================
# DASHBOARD DES RESULTATS
# ==========================================================

st.markdown("---")
st.header("📈 Tableau de bord des résultats")

# ==========================================================
# RADAR CHART
# ==========================================================

categories = list(percent_scores.keys())
values = list(percent_scores.values())

# fermer le radar
categories += [categories[0]]
values += [values[0]]

radar = go.Figure()

radar.add_trace(
    go.Scatterpolar(
        r=values,
        theta=categories,
        fill="toself",
        name="Compétences",
        line=dict(color="#4C8BF5", width=3),
        fillcolor="rgba(76,139,245,0.35)"
    )
)

radar.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0,100]
        )
    ),
    showlegend=False,
    height=500,
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    title="Radar des compétences"
)

# ==========================================================
# TOP 3 METIERS
# ==========================================================

top3 = top_jobs[:3]

job_names = [j[0] for j in top3]
job_values = [round(j[1]*100) for j in top3]

jobs_fig = go.Figure()

jobs_fig.add_trace(

    go.Bar(

        y=job_names,

        x=job_values,

        orientation="h",

        marker_color=[
            "#4C8BF5",
            "#7C6CF5",
            "#AA5DF5"
        ],

        text=[f"{v}%" for v in job_values],

        textposition="outside"

    )

)

jobs_fig.update_layout(

    title="Top 3 métiers recommandés",

    xaxis=dict(range=[0,100]),

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    font=dict(color="white"),

    height=500

)

# ==========================================================
# AFFICHAGE DES DEUX GRAPHIQUES
# ==========================================================

left,right=st.columns([1.2,1])

with left:

    st.plotly_chart(
        radar,
        use_container_width=True
    )

with right:

    st.plotly_chart(
        jobs_fig,
        use_container_width=True
    )

# ==========================================================
# JUSTIFICATION DU METIER
# ==========================================================

st.markdown("---")

st.subheader("🎯 Pourquoi ce métier est recommandé ?")

st.success(f"**{job_reco}** est le métier présentant la meilleure compatibilité avec votre profil.")

details = job_details[job_reco][:4]

for element in details:

    st.markdown(

        f"""
✅ **{element['competency']}**

Bloc : *{element['block']}*

Score : **{round(element['score']*100)}%**
"""

    )

# ==========================================================
# FORCES / FAIBLESSES
# ==========================================================

st.markdown("---")

col1,col2=st.columns(2)

with col1:

    st.subheader("💪 Points forts")

    for block,score in strengths:

        st.success(
            f"{block} — {round(score*100)}%"
        )

with col2:

    st.subheader("📈 Axes d'amélioration")

    for block,score in weaknesses:

        st.warning(
            f"{block} — {round(score*100)}%"
        )

# ==========================================================
# COMPETENCES DETECTEES PAR SBERT
# ==========================================================

st.markdown("---")

st.subheader("🧠 Compétences détectées")

tabs=st.tabs(

    list(matched_micro_skills.keys())

)

for tab,block in zip(

    tabs,

    matched_micro_skills.keys()

):

    with tab:

        for comp in matched_micro_skills[block][:4]:

            st.markdown(

                f"""
**{comp['competency']}**

Micro-compétence reconnue :

`{comp['micro_skill']}`

Score : **{round(comp['score']*100)}%**

---
"""

            )

# ==========================================================
# RESUME AUTOMATIQUE
# ==========================================================

st.markdown("---")

st.subheader("📋 Résumé du profil")

resume=f"""

Votre profil présente un score global de **{global_score}%**.

Le métier présentant la meilleure adéquation est :

**{job_reco}**

Vos principaux points forts sont :

• {strengths[0][0]}

• {strengths[1][0]}

Les compétences nécessitant un renforcement sont :

• {weaknesses[0][0]}

• {weaknesses[1][0]}

"""

st.info(resume)
# ==========================================================
# IA GENERATIVE
# ==========================================================

st.markdown("---")

st.header("🤖 Analyse IA Personnalisée")

context = build_context(inputs, results)

bio_placeholder = st.empty()
plan_placeholder = st.empty()

# ---------------- BIO ----------------

if "bio_text" not in st.session_state:

    bio_placeholder.markdown("""

### 🧠 Génération de votre bio...

<div class="loader-bar"></div>

""", unsafe_allow_html=True)

    st.session_state["bio_text"] = generate_bio(context)

    time.sleep(0.4)

    bio_placeholder.empty()

# ---------------- PLAN ----------------

if "plan_text" not in st.session_state:

    plan_placeholder.markdown("""

### 📚 Génération du plan d'apprentissage...

<div class="loader-bar"></div>

""", unsafe_allow_html=True)

    st.session_state["plan_text"] = generate_learning_plan(context)

    time.sleep(0.4)

    plan_placeholder.empty()

bio = st.session_state["bio_text"]
plan = st.session_state["plan_text"]

left, right = st.columns(2)

with left:

    st.subheader("👤 Bio professionnelle")

    st.markdown(
        f"""
<div style="background:#1f1f1f;
padding:20px;
border-radius:12px;
border:1px solid #333;">
{bio}
</div>
""",
        unsafe_allow_html=True,
    )

with right:

    st.subheader("📚 Plan de progression")

    st.markdown(
        f"""
<div style="background:#1f1f1f;
padding:20px;
border-radius:12px;
border:1px solid #333;">
{plan}
</div>
""",
        unsafe_allow_html=True,
    )

# ==========================================================
# EXPORT DES GRAPHIQUES
# ==========================================================

os.makedirs("temp", exist_ok=True)

radar_path = "temp/radar.png"
jobs_path = "temp/jobs.png"

try:

    radar.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="black")
    )

    jobs_fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="black")
    )

    radar.write_image(
        radar_path,
        engine="kaleido",
        scale=2
    )

    jobs_fig.write_image(
        jobs_path,
        engine="kaleido",
        scale=2
    )

except:

    radar_path = None
    jobs_path = None

# ==========================================================
# PDF
# ==========================================================

st.markdown("---")

st.header("📄 Rapport professionnel")

with tempfile.NamedTemporaryFile(
    delete=False,
    suffix=".pdf"
) as tmp:

    pdf_path = tmp.name

generate_pdf(

    pdf_path,

    percent_scores,

    job_reco,

    bio,

    plan,

    radar_path,

    jobs_path

)

with open(pdf_path, "rb") as pdf:

    st.download_button(

        "📥 Télécharger le rapport AISCA",

        data=pdf.read(),

        file_name="Rapport_AISCA.pdf",

        mime="application/pdf",

        use_container_width=True

    )

# ==========================================================
# FIN
# ==========================================================

st.markdown("---")

st.caption(
    "AISCA • Analyse Sémantique des Compétences • Version 2.0"
)