import json
import numpy as np
from sentence_transformers import SentenceTransformer, util

# Charger le modèle SBERT
model = SentenceTransformer("all-MiniLM-L6-v2")

# Charger les compétences
with open("data/competencies.json", "r") as f:
    competency_blocks = json.load(f)

# Charger les métiers
with open("data/jobs.json", "r") as f:
    job_profiles = json.load(f)


def compute_block_scores(user_text):
    """
    Calcule un score pour chaque bloc de compétences
    """
    user_embedding = model.encode(user_text, convert_to_tensor=True)
    block_scores = {}

    for block, skills in competency_blocks.items():
        skill_embeddings = model.encode(skills, convert_to_tensor=True)
        similarities = util.cos_sim(user_embedding, skill_embeddings)
        max_similarity = float(similarities.max())
        block_scores[block] = max_similarity

    return block_scores


def compute_job_recommendation(block_scores):
    """
    Détermine le métier le plus adapté selon les scores
    """
    job_scores = {}

    for job, required_skills in job_profiles.items():
        scores = []
        for skill in required_skills:
            # Cherche dans quel bloc est cette compétence
            for block, skills in competency_blocks.items():
                if skill in skills:
                    scores.append(block_scores[block])

        job_scores[job] = np.mean(scores)

    best_job = max(job_scores, key=job_scores.get)
    return best_job, job_scores


def analyze_user(user_text):
    """
    Fonction principale appelée par l'application Streamlit (Personne B)
    """
    block_scores = compute_block_scores(user_text)
    best_job, job_scores = compute_job_recommendation(block_scores)

    return {
        "block_scores": block_scores,
        "job_recommendation": best_job,
        "job_scores": job_scores

    }
