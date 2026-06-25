def build_context(inputs, results):
    """
    Construit un contexte RAG simple et structuré pour Gemini.
    """

    # ==========================================
    # Scores SBERT
    # ==========================================
    scores = {
        bloc: int(score * 100)
        for bloc, score in results["block_scores"].items()
    }

    job = results["job_recommendation"]

    strengths = ", ".join(
        [f"{bloc} ({int(score*100)}%)"
         for bloc, score in results["strengths"]]
    )

    weaknesses = ", ".join(
        [f"{bloc} ({int(score*100)}%)"
         for bloc, score in results["weaknesses"]]
    )

    # ==========================================
    # Compétences reconnues
    # ==========================================
    detected = []

    for block in results["matched_competencies"]:

        for comp in results["matched_competencies"][block][:2]:
            detected.append(comp["competency"])

    detected = ", ".join(detected)

    # ==========================================
    # Profil utilisateur
    # ==========================================
    projects = " | ".join(
        [p for p in inputs["projects"] if p.strip()]
    )

    tech = ", ".join(inputs["tech_skills"]) if inputs["tech_skills"] else "Aucune"

    soft = ", ".join(inputs["soft_skills"]) if inputs["soft_skills"] else "Aucune"

    # ==========================================
    # Contexte envoyé à Gemini
    # ==========================================
    context = f"""
PROFIL

Domaine : {inputs['domain_choice']}
Formation : {inputs['education']}
Expérience : {inputs['experience']}

Compétences techniques :
{tech}

Soft skills :
{soft}

Projets :
{projects}

ANALYSE SBERT

Métier recommandé :
{job}

Scores :
{scores}

Points forts :
{strengths}

Axes d'amélioration :
{weaknesses}

Compétences détectées :
{detected}

INSTRUCTION

Tu es un expert RH.

À partir du profil :

- rédige une bio professionnelle de 5 lignes maximum ;
- rédige un plan d'apprentissage composé de :
  • 3 objectifs,
  • 3 recommandations,
  • une courte conclusion.

Le texte doit être personnalisé, professionnel et ne jamais recopier le contexte.
"""

    return context.strip()