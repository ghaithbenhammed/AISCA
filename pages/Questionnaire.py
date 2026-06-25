import streamlit as st

st.set_page_config(page_title="AISCA – Questionnaire", layout="wide")

# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
<h1 style='text-align:center;'>
📝 Questionnaire Professionnel
</h1>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<p style='text-align:center;font-size:17px;color:gray'>
Répondez aux questions ci-dessous afin de permettre une analyse
sémantique précise de votre profil et de recevoir une
recommandation métier personnalisée.
</p>
""",
    unsafe_allow_html=True,
)

st.divider()

# ============================================================
# EXPERIENCES PROJETS
# ============================================================

st.subheader("📝 Expériences projets")

st.info(
"""
Pour obtenir une analyse plus pertinente, décrivez vos projets
en précisant :

• l'objectif du projet

• les technologies utilisées

• les méthodes IA / Data employées

• les résultats obtenus
"""
)

placeholder_project = """
Exemple :

Développement d'un modèle de classification des clients
avec Python, Pandas et Scikit-Learn.

Prétraitement des données, Feature Engineering,
Random Forest puis évaluation (Accuracy : 91%).

Le modèle a permis d'améliorer la prédiction
du churn client.
"""

projet_1 = st.text_area(
    "Projet 1 (obligatoire)",
    placeholder=placeholder_project,
    height=170,
)

projet_2 = st.text_area(
    "Projet 2 (obligatoire)",
    placeholder=placeholder_project,
    height=170,
)

projet_3 = st.text_area(
    "Projet 3 (optionnel)",
    placeholder=placeholder_project,
    height=170,
)

st.divider()

# ============================================================
# COMPETENCES TECHNIQUES
# ============================================================

st.subheader("⚙️ Compétences techniques")

tech_skills = st.multiselect(
    "Sélectionnez les compétences que vous maîtrisez :",
    [
        "Python",
        "SQL",
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "Computer Vision",
        "Power BI",
        "Excel avancé",
        "Data Engineering",
        "Cloud (AWS / Azure / GCP)",
        "API REST",
        "DevOps"
    ]
)

# ============================================================
# FRAMEWORKS
# ============================================================

st.subheader("🛠️ Bibliothèques & Frameworks")

frameworks = st.multiselect(
    "Quels outils utilisez-vous régulièrement ?",
    [
        "Pandas",
        "NumPy",
        "Scikit-Learn",
        "TensorFlow",
        "PyTorch",
        "Hugging Face",
        "spaCy",
        "Matplotlib",
        "Seaborn",
        "Plotly",
        "Git",
        "Docker",
        "FastAPI",
        "Streamlit"
    ]
)

st.divider()

# ============================================================
# TYPES DE PROJETS
# ============================================================

st.subheader("📂 Types de projets réalisés")

project_types = st.multiselect(
    "Sélectionnez les types de projets que vous avez déjà réalisés :",
    [
        "Analyse de données",
        "Classification",
        "Régression",
        "Clustering",
        "NLP",
        "Computer Vision",
        "Dashboard BI",
        "ETL",
        "API IA",
        "Chatbot",
        "MLOps"
    ]
)

st.divider()
# ============================================================
# DOMAINE D'INTERET
# ============================================================

st.subheader("🎯 Domaine d'intérêt principal")

domain_choice = st.radio(
    "Quel domaine vous attire le plus ?",
    [
        "Analyse de données",
        "Machine Learning",
        "NLP & IA Générative"
    ],
    horizontal=True
)

st.divider()

# ============================================================
# AUTO-EVALUATION
# ============================================================

st.subheader("📊 Auto-évaluation des compétences")

st.caption(
    "Évaluez votre niveau de maîtrise sur une échelle de 1 (Débutant) à 5 (Expert)."
)

col1, col2, col3 = st.columns(3)

with col1:

    python_level = st.slider(
        "Python",
        1, 5, 3
    )

    viz_level = st.slider(
        "Visualisation de données",
        1, 5, 3
    )

with col2:

    ml_level = st.slider(
        "Machine Learning",
        1, 5, 2
    )

    stats_level = st.slider(
        "Statistiques",
        1, 5, 2
    )

with col3:

    nlp_level = st.slider(
        "NLP",
        1, 5, 2
    )

    cloud_level = st.slider(
        "Cloud",
        1, 5, 2
    )

st.divider()

# ============================================================
# SOFT SKILLS
# ============================================================

st.subheader("🤝 Soft Skills")

soft_skills = st.multiselect(
    "Sélectionnez vos principales qualités :",
    [
        "Communication",
        "Travail d'équipe",
        "Résolution de problèmes",
        "Adaptabilité",
        "Autonomie",
        "Esprit d'analyse",
        "Gestion de projet",
        "Créativité"
    ]
)

st.divider()

# ============================================================
# INFORMATIONS COMPLEMENTAIRES
# ============================================================

st.subheader("🎓 Informations complémentaires")

col1, col2 = st.columns(2)

with col1:

    years_exp = st.selectbox(
        "Années d'expérience",
        [
            "0-1 an",
            "1-2 ans",
            "2-3 ans",
            "3-5 ans",
            "5+ ans"
        ]
    )

    education = st.selectbox(
        "Niveau d'étude",
        [
            "Licence",
            "Master",
            "Ingénieur",
            "Doctorat"
        ]
    )

with col2:

    certifications = st.multiselect(
        "Certifications obtenues",
        [
            "AWS",
            "Azure",
            "Google Cloud",
            "IBM",
            "Oracle",
            "Databricks",
            "Aucune"
        ]
    )

    languages = st.multiselect(
        "Langues maîtrisées",
        [
            "Français",
            "Anglais",
            "Arabe",
            "Espagnol",
            "Allemand"
        ]
    )

st.divider()

# ============================================================
# OBJECTIF PROFESSIONNEL
# ============================================================

st.subheader("🚀 Objectif professionnel")

career_goal = st.selectbox(
    "Quel est votre objectif actuel ?",
    [
        "Trouver un stage",
        "Trouver une alternance",
        "Trouver un premier emploi",
        "Évoluer vers un poste plus avancé",
        "Se reconvertir vers la Data / IA"
    ]
)

st.divider()
# ============================================================
# PACK FINAL DES DONNÉES
# ============================================================

user_inputs = {

    # ----------------------------------
    # Projets
    # ----------------------------------
    "projects": [
        projet_1,
        projet_2,
        projet_3
    ],

    # ----------------------------------
    # Compétences
    # ----------------------------------
    "tech_skills": tech_skills,
    "frameworks": frameworks,
    "project_types": project_types,

    # ----------------------------------
    # Domaine
    # ----------------------------------
    "domain_choice": domain_choice,

    # ----------------------------------
    # Auto-évaluation
    # ----------------------------------
    "likert": {

        "python": python_level,
        "viz": viz_level,
        "ml": ml_level,
        "stats": stats_level,
        "nlp": nlp_level,
        "cloud": cloud_level

    },

    # ----------------------------------
    # Soft Skills
    # ----------------------------------
    "soft_skills": soft_skills,

    # ----------------------------------
    # Informations générales
    # ----------------------------------
    "experience": years_exp,
    "education": education,
    "certifications": certifications,
    "languages": languages,
    "career_goal": career_goal

}

# ============================================================
# VALIDATION
# ============================================================

def form_is_valid():

    errors = []

    # ------------------------------
    # Vérification projets
    # ------------------------------

    if not projet_1.strip():
        errors.append("❌ Le Projet 1 est obligatoire.")

    elif len(projet_1.strip()) < 80:
        errors.append(
            "❌ Le Projet 1 est trop court. Décrivez le contexte, les technologies et les résultats."
        )

    if not projet_2.strip():
        errors.append("❌ Le Projet 2 est obligatoire.")

    elif len(projet_2.strip()) < 80:
        errors.append(
            "❌ Le Projet 2 est trop court. Décrivez le contexte, les technologies et les résultats."
        )

    # ------------------------------
    # Compétences techniques
    # ------------------------------

    if len(tech_skills) == 0:
        errors.append(
            "❌ Sélectionnez au moins une compétence technique."
        )

    # ------------------------------
    # Frameworks
    # ------------------------------

    if len(frameworks) == 0:
        errors.append(
            "❌ Sélectionnez au moins un framework ou outil."
        )

    # ------------------------------
    # Types de projets
    # ------------------------------

    if len(project_types) == 0:
        errors.append(
            "❌ Sélectionnez au moins un type de projet."
        )

    # ------------------------------
    # Affichage erreurs
    # ------------------------------

    if errors:

        st.error("Le questionnaire contient quelques erreurs :")

        for err in errors:
            st.write(err)

        return False

    return True


# ============================================================
# BOUTON
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,2,1])

with col2:

    submitted = st.button(
        "🚀 Lancer l'analyse de mon profil",
        use_container_width=True
    )

# ============================================================
# ENVOI VERS LA PAGE RESULTATS
# ============================================================

if submitted:

    if form_is_valid():

        st.session_state["user_inputs"] = user_inputs

        st.switch_page("pages/Résultats.py")