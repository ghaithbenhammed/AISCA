import streamlit as st
from semantic_engine import analyze_user

st.set_page_config(page_title="AISCA – Questionnaire", layout="wide")

st.title("📝 Questionnaire Professionnel")

st.write("Merci de répondre aux questions suivantes...")

# -----------------------------
# 1) PROJETS (TEXTE LIBRE)
# -----------------------------
st.subheader("📝 Vos expériences projets")

projet_1 = st.text_area("Projet 1 : Décrivez une expérience technique importante", 
                        placeholder="Exemple : j’ai développé un modèle de classification…", height=130)

projet_2 = st.text_area("Projet 2 : Décrivez une autre expérience", 
                        placeholder="Exemple : j’ai automatisé un pipeline ETL…", height=130)

projet_3 = st.text_area("Projet 3 : (optionnel)", placeholder="Décrivez un troisième projet…", height=130)

# -----------------------------
# 2) COMPÉTENCES TECHNIQUES
# -----------------------------
st.subheader("⚙️ Compétences techniques maîtrisées")

tech_skills = st.multiselect(
    "Sélectionnez les compétences que vous maîtrisez :",
    [
        "Python", "SQL", "Power BI", "Excel avancé", "Machine Learning",
        "Deep Learning", "NLP", "Computer Vision", "Data Engineering",
        "DevOps", "Cloud (AWS/GCP/Azure)", "API REST"
    ]
)

# -----------------------------
# 3) DOMAINE PRÉFÉRÉ (3 choix)
# -----------------------------
st.subheader("🔍 Quel domaine vous attire le plus ?")

domain_choice = st.radio(
    "Choisissez une seule réponse :",
    ["Analyse de données", "Machine Learning", "NLP & IA Générative"]
)

# -----------------------------
# 4) LIKERT (AUTO-ÉVALUATION)
# -----------------------------
st.subheader("📊 Auto-évaluation (1 = débutant, 5 = expert)")

colA, colB, colC = st.columns(3)

with colA:
    python_level = st.slider("Niveau Python", 1, 5, 3)
    viz_level = st.slider("Visualisation de données", 1, 5, 3)

with colB:
    ml_level = st.slider("Machine Learning", 1, 5, 2)
    stats_level = st.slider("Statistiques", 1, 5, 2)

with colC:
    nlp_level = st.slider("NLP", 1, 5, 1)
    cloud_level = st.slider("Cloud", 1, 5, 1)

# -----------------------------
# 5) SOFT SKILLS
# -----------------------------
st.subheader("🤝 Soft Skills")

communication = st.checkbox("Communication")
teamwork = st.checkbox("Travail d'équipe")
problem_solving = st.checkbox("Résolution de problèmes")
adaptability = st.checkbox("Adaptabilité")

soft_skills = []
if communication: soft_skills.append("Communication")
if teamwork: soft_skills.append("Travail d'équipe")
if problem_solving: soft_skills.append("Résolution de problèmes")
if adaptability: soft_skills.append("Adaptabilité")

# -----------------------------
# 6) EXPÉRIENCE & FORMATION
# -----------------------------
st.subheader("🎓 Informations complémentaires")

years_exp = st.selectbox(
    "Années d'expérience :",
    ["0-1 an", "1-2 ans", "2-3 ans", "3-5 ans", "5+ ans"]
)

education = st.radio(
    "Niveau d'étude :",
    ["Licence", "Master", "Ingénieur", "Doctorat"]
)

certified = st.checkbox("Avez-vous une certification ? (Azure, AWS, Google, IBM, etc.)")

# -----------------------------
# 7) PACK DES RÉPONSES
# -----------------------------
user_inputs = {
    "projects": [projet_1, projet_2, projet_3],
    "tech_skills": tech_skills,
    "domain_choice": domain_choice,
    "likert": {
        "python": python_level,
        "viz": viz_level,
        "ml": ml_level,
        "stats": stats_level,
        "nlp": nlp_level,
        "cloud": cloud_level
    },
    "soft_skills": soft_skills,
    "experience": years_exp,
    "education": education,
    "certified": certified
}


# --- bouton ---
center = st.columns(3)[1]
with center:
    submitted = st.button("🔍 Analyser mon profil", use_container_width=True)

# --- si bouton cliqué, stocker les réponses ---
if submitted:
    st.session_state["user_inputs"] = user_inputs
    st.switch_page("pages/Résultats.py")
