import json
import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer, util


# ====================================================
# 1) CHARGEMENT UNIQUE ET CACHE DU MODÈLE SBERT
# ====================================================
@st.cache_resource(show_spinner=False)
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()


# ====================================================
# 2) CHARGEMENT DES COMPÉTENCES
# ====================================================
with open("data/competencies.json", "r", encoding="utf-8") as f:
    competency_blocks = json.load(f)

with open("data/jobs.json", "r", encoding="utf-8") as f:
    job_profiles = json.load(f)


# ====================================================
# 3) PRÉ-CALCUL DES EMBEDDINGS DES MICRO-COMPÉTENCES
# ====================================================
@st.cache_resource(show_spinner=False)
def compute_competency_embeddings():
    comp_emb = {}

    for block, competencies in competency_blocks.items():
        comp_emb[block] = {}

        for comp_name, micro_list in competencies.items():
            embeddings = model.encode(micro_list, convert_to_tensor=True)
            comp_emb[block][comp_name] = embeddings

    return comp_emb


COMPETENCY_EMBEDDINGS = compute_competency_embeddings()


# ====================================================
# 4) SCORE DES BLOCS (ULTRA OPTIMISÉ)
# ====================================================
def compute_block_scores(user_text):
    user_embedding = model.encode(user_text, convert_to_tensor=True)
    block_scores = {}

    for block, competencies in COMPETENCY_EMBEDDINGS.items():
        comp_scores = []

        for comp_name, micro_embeddings in competencies.items():
            similarities = util.cos_sim(user_embedding, micro_embeddings)
            comp_scores.append(float(similarities.max()))

        block_scores[block] = float(np.mean(comp_scores))

    return block_scores


# ====================================================
# 5) RECOMMANDATION MÉTIER
# ====================================================
def compute_job_recommendation(block_scores):
    job_scores = {}

    for job, required_skills in job_profiles.items():
        scores = []

        for skill in required_skills:
            for block in competency_blocks:
                if skill in competency_blocks[block]:
                    scores.append(block_scores[block])

        job_scores[job] = float(np.mean(scores)) if scores else 0.0

    best_job = max(job_scores, key=job_scores.get)
    return best_job, job_scores


# ====================================================
# 6) FONCTION FINALE APPELÉE PAR TON FRONTEND
# ====================================================
def analyze_user(user_text):
    block_scores = compute_block_scores(user_text)
    best_job, job_scores = compute_job_recommendation(block_scores)

    return {
        "block_scores": block_scores,
        "job_recommendation": best_job,
        "job_scores": job_scores
    }
