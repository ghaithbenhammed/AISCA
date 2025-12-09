import json
import numpy as np
from sentence_transformers import SentenceTransformer, util

# Charger le modèle SBERT
model = SentenceTransformer("all-MiniLM-L6-v2")

# Charger les compétences (structure : Bloc → Compétences → Micro-compétences)
with open("data/competencies.json", "r") as f:
    competency_blocks = json.load(f)

# Charger les métiers
with open("data/jobs.json", "r") as f:
    job_profiles = json.load(f)


def flatten_block(block_data):
    """
    Prend un bloc de compétences et retourne une liste
    contenant :
    - les compétences
    - les micro-compétences associées
    """
    flat_list = []
    for comp, micro_comp_list in block_data.items():
        flat_list.append(comp)                    # compétence principale
        flat_list.extend(micro_comp_list)         # micro-compétences
    return flat_list


def compute_block_scores(user_text):
    """
    Calcule un score pour chaque bloc de compétences (avec micro-compétences)
    """
    user_embedding = model.encode(user_text, convert_to_tensor=True)
    block_scores = {}

    for block, skills_dict in competency_blocks.items():
        # Aplatir compétences + microcompétences
        skill_list = flatten_block(skills_dict)

        # Embeddings de toutes les compétences du bloc
        skill_embeddings = model.encode(skill_list, convert_to_tensor=True)
        similarities = util.cos_sim(user_embedding, skill_embeddings)

        # Score = meilleure similarité du bloc
        max_similarity = float(similarities.max())
        block_scores[block] = max_similarity

    return block_scores


def compute_job_recommendation(block_scores):
    """
    Détermine le métier le plus adapté selon les scores des blocs
    """
    job_scores = {}

    for job, required_skills in job_profiles.items():
        scores = []

        for skill in required_skills:
            # Trouver dans quel bloc est cette compétence
            for block, skills_dict in competency_blocks.items():
                if skill in skills_dict:  # match compétence principale
                    scores.append(block_scores[block])

        job_scores[job] = np.mean(scores)

    best_job = max(job_scores, key=job_scores.get)
    return best_job, job_scores


def analyze_user(user_text):
    """
    Fonction appelée par Streamlit (Personne B)
    """
    block_scores = compute_block_scores(user_text)
    best_job, job_scores = compute_job_recommendation(block_scores)

    return {
        "block_scores": block_scores,
        "job_recommendation": best_job,
        "job_scores": job_scores

    }
