AISCA — Analyse Sémantique des Compétences & Recommandation de Métiers

Projet d’IA Générative & Semantic Matching – 2024 / 2025
Par : Ghaith BEN HAMMED / Chaïma ASTITOU

📌 Description du Projet

AISCA est une application interactive développée en Python + Streamlit permettant :

d’analyser automatiquement les compétences d’un utilisateur

de calculer la similarité sémantique de son profil via SBERT (Sentence-BERT)

de recommander le métier le plus pertinent

de générer automatiquement une bio professionnelle et un plan d’apprentissage personnalisé grâce au modèle Gemini 2.5 Flash (Google)

de produire un rapport PDF professionnel contenant graphiques + synthèse IA

🚀 Fonctionnalités principales
🔍 Analyse SBERT (Semantic Similarity)

Extraction des informations clés du questionnaire

Encodage SBERT via all-MiniLM-L6-v2

Matching sémantique contre :

4 blocs de compétences

plusieurs métiers cibles

📊 Visualisation Interactive

Les résultats sont affichés via Plotly :

Doughnut Chart de répartition des scores

Bar Chart horizontal des compétences

Interactif, fluide et responsive

🤖 IA Générative – Gemini 2.5 Flash

L’IA génère automatiquement :

une bio professionnelle courte (6 lignes)

un plan d’apprentissage structuré (10 lignes max)

un texte clair, synthétique et orienté Data/IA

📄 Génération d’un Rapport PDF Pro

Le PDF inclut :

Graphiques exportés en haute résolution

Forces & faiblesses du profil

Métier recommandé

Bio + Plan d’apprentissage IA

Mise en page avec header/footer & pagination

🧩 Architecture du Projet
AISCA/
│── app.py → Page d'accueil
│── semantic_engine.py → Analyse SBERT
│── genai.py → Appels API Gemini 2.5 Flash
│── rag_context.py → Construction du contexte IA
│── README.md → Documentation
│
├── data/
│ ├── competencies.json → Blocs de compétences
│ └── jobs.json → Profils métiers
│
├── pages/
│ ├── Questionnaire.py → Questionnaire utilisateur
│ └── Résultats.py → Analyse + IA + PDF
│
├── utils/
│ └── pdf_generator.py → Génération PDF professionnel
│
├── temp/ → Export images (ignoré)
│
└── .gitignore → Exclusions Git

🛠️ Tech Stack
Technologie Rôle
Python 3.12 Base du projet
Streamlit Interface web
SentenceTransformers (SBERT) Similarité sémantique
Google Gemini API – 2.5 Flash IA générative
Plotly Visualisations
ReportLab Génération PDF
Kaleido Export des graphiques
📦 Installation
git clone https://github.com/ghaithbenhammed/AISCA.git
cd AISCA
pip install -r requirements.txt
streamlit run app.py

👨‍🏫 Encadrement & Exigences respectées

✔ Analyse sémantique SBERT
✔ RAG & construction de contexte
✔ IA générative Gemini
✔ Interface Streamlit structurée
✔ UX fluide + animations
✔ Rapport PDF professionnel
✔ Validation des champs obligatoires

📘 Licence

Projet académique — reproduction autorisée avec citation.
