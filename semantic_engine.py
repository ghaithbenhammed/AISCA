import json
import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer, util


# ====================================================
# CHARGEMENT UNIQUE DU MODELE SBERT
# ====================================================

@st.cache_resource(show_spinner=False)
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


model = load_model()


# ====================================================
# CHARGEMENT DES DONNEES
# ====================================================

with open("data/competencies.json", "r", encoding="utf-8") as f:
    competency_blocks = json.load(f)

with open("data/jobs.json", "r", encoding="utf-8") as f:
    job_profiles = json.load(f)


# ====================================================
# PRE-CALCUL DES EMBEDDINGS
# ====================================================

@st.cache_resource(show_spinner=False)
def build_embeddings():

    embeddings = {}

    for block, competencies in competency_blocks.items():

        embeddings[block] = {}

        for competency, micro_skills in competencies.items():

            embeddings[block][competency] = {
                "skills": micro_skills,
                "embeddings": model.encode(
                    micro_skills,
                    convert_to_tensor=True
                )
            }

    return embeddings


COMPETENCY_EMBEDDINGS = build_embeddings()


# ====================================================
# ANALYSE DES BLOCS
# ====================================================

def compute_block_scores(user_text):

    user_embedding = model.encode(user_text, convert_to_tensor=True)

    block_scores = {}

    matched_competencies = {}

    matched_micro_skills = {}

    for block, competencies in COMPETENCY_EMBEDDINGS.items():

        competency_scores = []

        matched_competencies[block] = []

        matched_micro_skills[block] = []

        for competency_name, values in competencies.items():

            similarities = util.cos_sim(
                user_embedding,
                values["embeddings"]
            )[0]

            similarities = similarities.cpu().numpy()

            best_index = int(np.argmax(similarities))
            best_score = float(similarities[best_index])

            competency_scores.append(best_score)

            matched_competencies[block].append({
                "competency": competency_name,
                "score": round(best_score, 3)
            })

            matched_micro_skills[block].append({
                "competency": competency_name,
                "micro_skill": values["skills"][best_index],
                "score": round(best_score, 3)
            })

        block_scores[block] = float(np.mean(competency_scores))

        matched_competencies[block] = sorted(
            matched_competencies[block],
            key=lambda x: x["score"],
            reverse=True
        )

        matched_micro_skills[block] = sorted(
            matched_micro_skills[block],
            key=lambda x: x["score"],
            reverse=True
        )

    return block_scores, matched_competencies, matched_micro_skills


# ====================================================
# RECOMMANDATION METIER
# ====================================================

def compute_job_recommendation(block_scores):

    job_scores = {}

    job_details = {}

    for job, competencies in job_profiles.items():

        scores = []

        explanations = []

        for competency in competencies:

            for block, block_competencies in competency_blocks.items():

                if competency in block_competencies:

                    score = block_scores[block]

                    scores.append(score)

                    explanations.append({
                        "block": block,
                        "competency": competency,
                        "score": round(score, 3)
                    })

        job_scores[job] = float(np.mean(scores)) if scores else 0

        job_details[job] = sorted(
            explanations,
            key=lambda x: x["score"],
            reverse=True
        )

    best_job = max(job_scores, key=job_scores.get)

    return best_job, job_scores, job_details


# ====================================================
# ANALYSE COMPLETE
# ====================================================

def analyze_user(user_text):

    (
        block_scores,
        matched_competencies,
        matched_micro_skills
    ) = compute_block_scores(user_text)

    (
        best_job,
        job_scores,
        job_details
    ) = compute_job_recommendation(block_scores)

    sorted_blocks = sorted(
        block_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    strengths = sorted_blocks[:2]

    weaknesses = sorted_blocks[-2:]

    return {

        "block_scores": block_scores,

        "job_scores": job_scores,

        "job_recommendation": best_job,

        "job_details": job_details,

        "matched_competencies": matched_competencies,

        "matched_micro_skills": matched_micro_skills,

        "strengths": strengths,

        "weaknesses": weaknesses
    }