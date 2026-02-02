import streamlit as st

st.set_page_config(page_title="AISCA – Questionnaire", layout="wide")

# ===============================
# HEADER
# ===============================
st.markdown(
    "<h1 style='text-align:center;'>📝 Questionnaire Professionnel</h1>",
    unsafe_allow_html=True,
)
st.write(
    "<p style='text-align:center; font-size:16px;'>Merci de répondre aux questions suivantes pour permettre une analyse complète et précise de votre profil.</p>",
    unsafe_allow_html=True,
)

# ============================================================
# 1) PROJETS (OBLIGATOIRE)
# ============================================================
st.subheader("📝 Vos expériences projets")

projet_1 = st.text_area(
    "Projet 1 (obligatoire)",
    placeholder="Exemple : j’ai développé un modèle de classification…",
    height=120,
)

projet_2 = st.text_area(
    "Projet 2 (obligatoire)",
    placeholder="Exemple : j’ai automatisé un pipeline ETL…",
    height=120,
)

projet_3 = st.text_area(
    "Projet 3 (optionnel)",
    placeholder="Décrivez un troisième projet…",
    height=120,
)

# ============================================================
# 2) COMPÉTENCES TECHNIQUES (OBLIGATOIRE)
# ============================================================
st.subheader("⚙️ Compétences techniques (au moins 1 requise)")

tech_skills = st.multiselect(
    "Sélectionnez vos compétences :",
    [
        "Python", "SQL", "Power BI", "Excel avancé", "Machine Learning",
        "Deep Learning", "NLP", "Computer Vision", "Data Engineering",
        "DevOps", "Cloud (AWS/GCP/Azure)", "API REST",
    ],
)

# ============================================================
# 3) DOMAINE PRÉFÉRÉ
# ============================================================
st.subheader("🔍 Domaine d’intérêt principal")

domain_choice = st.radio(
    "Choisissez votre préférence :",
    ["Analyse de données", "Machine Learning", "NLP & IA Générative"],
)

# ============================================================
# 4) AUTO-EVALUATION
# ============================================================
st.subheader("📊 Auto-évaluation (Score 1 → 5)")

colA, colB, colC = st.columns(3)

with colA:
    python_level = st.slider("Python", 1, 5, 3)
    viz_level = st.slider("Visualisation", 1, 5, 3)

with colB:
    ml_level = st.slider("Machine Learning", 1, 5, 2)
    stats_level = st.slider("Statistiques", 1, 5, 2)

with colC:
    nlp_level = st.slider("NLP", 1, 5, 1)
    cloud_level = st.slider("Cloud", 1, 5, 1)

# ============================================================
# 5) SOFT SKILLS
# ============================================================
st.subheader("🤝 Soft Skills")

soft_skills = []
if st.checkbox("Communication"): soft_skills.append("Communication")
if st.checkbox("Travail d'équipe"): soft_skills.append("Travail d'équipe")
if st.checkbox("Résolution de problèmes"): soft_skills.append("Résolution de problèmes")
if st.checkbox("Adaptabilité"): soft_skills.append("Adaptabilité")

# ============================================================
# 6) INFORMATIONS GÉNÉRALES
# ============================================================
st.subheader("🎓 Informations complémentaires")

years_exp = st.selectbox(
    "Années d'expérience :",
    ["0-1 an", "1-2 ans", "2-3 ans", "3-5 ans", "5+ ans"],
)

education = st.radio("Niveau d'étude :", ["Licence", "Master", "Ingénieur", "Doctorat"])
certified = st.checkbox("Avez-vous une certification ? (Azure, AWS, Google, IBM, etc.)")

# ============================================================
# 7) PACK FINAL DES DONNÉES
# ============================================================
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
        "cloud": cloud_level,
    },
    "soft_skills": soft_skills,
    "experience": years_exp,
    "education": education,
    "certified": certified,
}

# ============================================================
# VALIDATION DES CHAMPS OBLIGATOIRES
# ============================================================
def form_is_valid():
    errors = []

    if not projet_1.strip():
        errors.append("❌ Le projet 1 est obligatoire.")
    if not projet_2.strip():
        errors.append("❌ Le projet 2 est obligatoire.")
    if len(tech_skills) == 0:
        errors.append("❌ Vous devez sélectionner au moins UNE compétence technique.")

    if errors:
        for e in errors:
            st.error(e)
        return False

    return True

# ============================================================
# BOUTON DE VALIDATION
# ============================================================
center = st.columns(3)[1]
with center:
    submitted = st.button("🚀 Analyser mon profil", use_container_width=True)

if submitted:
    if form_is_valid():
        st.session_state["user_inputs"] = user_inputs
        st.switch_page("pages/Résultats.py")
