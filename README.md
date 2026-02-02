# 🚀 AISCA — Analyse Sémantique des Compétences & Recommandation de Métiers

### 🧠 *Projet d’IA Générative – Master 2024 / 2025*  
**Par : Ghaith BEN HAMMED & Chaïma ASTITOU**

---

## 📌 Présentation du Projet

**AISCA** est une application interactive développée en **Python + Streamlit** permettant :

- d’analyser automatiquement les compétences d’un utilisateur  
- de calculer la **similarité sémantique** de son profil via **SBERT (Sentence-BERT)**  
- de recommander le **métier le plus pertinent**  
- de générer automatiquement :
  - une **bio professionnelle courte**
  - un **plan d’apprentissage personnalisé**
  - grâce au modèle **Gemini 2.5 Flash (Google AI)**  
- de produire un **rapport PDF professionnel** contenant :
  - graphiques (Plotly)
  - synthèse IA
  - forces & faiblesses  
  - métier recommandé

---

## 🚀 Fonctionnalités

### 🔍 Analyse SBERT (Semantic Similarity)  
- Extraction automatique des informations du questionnaire  
- Encodage via `all-MiniLM-L6-v2`  
- Matching sémantique contre :
  - 4 blocs de compétences  
  - Profils métiers prédéfinis  

---

### 📊 Visualisation Interactive (Plotly)

- Diagramme **Doughnut**  
- Diagramme **Bar Chart horizontal**  
- Animation fluide et responsive  
- Export haute résolution pour le PDF  

---

### 🤖 IA Générative — Gemini 2.5 Flash

L’IA génère automatiquement :

- Une **bio professionnelle courte** (max 6 lignes)
- Un **plan d’apprentissage structuré** (max 10 lignes)
- Un texte clair, synthétique et adapté aux métiers Data/IA

---

### 📄 Génération d’un Rapport PDF Professionnel

Le rapport PDF final contient :

- Graphiques en haute résolution  
- Forces & Faiblesses du profil  
- Métier recommandé  
- Bio professionnelle  
- Plan d’apprentissage AI  

---
AISCA/
│── app.py # Page d'accueil
│── semantic_engine.py # Analyse SBERT
│── genai.py # Appels API Gemini
│── rag_context.py # Construction du contexte IA
│── README.md # Documentation
│
├── data/
│ ├── competencies.json # Blocs de compétences
│ └── jobs.json # Profils métiers
│
├── pages/
│ ├── Questionnaire.py # Questionnaire utilisateur
│ └── Résultats.py # Analyse + IA + PDF
│
├── utils/
│ └── pdf_generator.py # Génération PDF professionnel
│
├── temp/ # Export des images pour PDF 
│
└── .gitignore

## 🛠️ Tech Stack

| Technologie | Rôle |
|------------|------|
| **Python 3.12** | Base du projet |
| **Streamlit** | Interface Web |
| **SentenceTransformers (SBERT)** | Similarité sémantique |
| **Google Gemini API – 2.5 Flash** | IA générative |
| **Plotly** | Visualisations |
| **ReportLab** | Export PDF |
| **Kaleido** | Export images haute résolution |

---

## 📦 Installation

```bash
git clone https://github.com/ghaithbenhammed/AISCA.git
cd AISCA
pip install -r requirements.txt
streamlit run app.py
```

Exigences respectées

✔ Analyse sémantique avec SBERT
✔ Approche RAG (construction d’un contexte IA structuré)
✔ IA générative Gemini 2.5 Flash
✔ Interface Streamlit fluide & ergonomique
✔ Visualisations modernes et responsives
✔ Export PDF professionnel
✔ Validation stricte du questionnaire
✔ Architecture claire et modulaire

📘 Licence

Projet académique — reproduction autorisée avec citation.

