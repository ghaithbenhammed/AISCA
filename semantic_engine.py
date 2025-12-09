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
    Calcule un score pour chaque bloc :
    - Score de compétence = max(micro-compétences)
    - Score du bloc = moyenne des compétences
    """
    user_embedding = model.encode(user_text, convert_to_tensor=True)
    block_scores = {}
 
    for block, competencies in competency_blocks.items():
        comp_scores = []
 
        for comp_name, micro_list in competencies.items():
            # Encode les micro-compétences
            micro_embeddings = model.encode(micro_list, convert_to_tensor=True)
            similarities = util.cos_sim(user_embedding, micro_embeddings)
 
            # Score de la compétence = meilleure micro-similarité
            comp_score = float(similarities.max())
            comp_scores.append(comp_score)
 
        # Score final du bloc = moyenne des scores compétences
        block_scores[block] = float(np.mean(comp_scores))
 
    return block_scores
 
 
def compute_job_recommendation(block_scores):
    """
    Recommande un métier selon les scores des blocs
    """
    job_scores = {}
 
    for job, required_skills in job_profiles.items():
        scores = []
 
        for skill in required_skills:
            # Trouver dans quel bloc est cette compétence
            for block, competencies in competency_blocks.items():
                if skill in competencies:
                    scores.append(block_scores[block])
 
        job_scores[job] = float(np.mean(scores))
 
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