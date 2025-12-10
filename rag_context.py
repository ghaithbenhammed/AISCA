def build_context(inputs, results):
    """
    Construit un contexte structuré pour la GénAI.
    Ce contexte est utilisé par Gemini pour générer :
    - bio professionnelle
    - plan d'apprentissage
    - résumé de profil
    """

    # -------------------------
    # 1) RÉCUPÉRATION DES INFOS
    # -------------------------
    scores = results["block_scores"]
    job_reco = results["job_recommendation"]
    job_scores = results["job_scores"]

    # Pourcentages arrondis
    percent_scores = {k: int(v * 100) for k, v in scores.items()}

    # -------------------------
    # 2) FORCES & FAIBLESSES
    # -------------------------
    sorted_scores = sorted(percent_scores.items(), key=lambda x: x[1], reverse=True)

    strengths = [f"{k} ({v}%)" for k, v in sorted_scores[:2]]
    weaknesses = [f"{k} ({v}%)" for k, v in sorted_scores[-2:]]

    # -------------------------
    # 3) PROJETS UTILISATEUR
    # -------------------------
    projects = "\n".join([p for p in inputs["projects"] if p.strip()])

    # -------------------------
    # 4) COMPÉTENCES TECHNIQUES
    # -------------------------
    tech_skills = ", ".join(inputs["tech_skills"]) if inputs["tech_skills"] else "Non spécifié"

    # -------------------------
    # 5) SOFT SKILLS
    # -------------------------
    soft_skills = ", ".join(inputs["soft_skills"]) if inputs["soft_skills"] else "Non spécifié"

    # -------------------------
    # 6) AUTO-ÉVALUATION LIKERT
    # -------------------------
    likert_txt = "\n".join([f"- {k} : {v}/5" for k, v in inputs["likert"].items()])

    # -------------------------
    # 7) CONSTRUCTION DU CONTEXTE
    # -------------------------
    context = f"""
======================
PROFIL UTILISATEUR
======================
Projets déclarés :
{projects}

Compétences techniques déclarées :
{tech_skills}

Soft skills :
{soft_skills}

Auto-évaluation :
{likert_txt}

Objectif utilisateur :
{inputs['domain_choice']}


======================
ANALYSE SBERT
======================
Scores par bloc de compétence :
{percent_scores}

Forces détectées :
{strengths}

Faiblesses détectées :
{weaknesses}

Métier recommandé :
{job_reco}

Détail des scores métiers :
{job_scores}


======================
INSTRUCTIONS POUR L'IA
======================
Utilise ces informations pour :
- générer une bio professionnelle courte
- générer un plan de progression structuré
- résumer le profil de manière claire
- expliquer les forces et faiblesses
- adapter le niveau de langage à un étudiant de master

Réponds toujours de manière structurée et professionnelle.
"""

    return context
