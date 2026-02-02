def build_context(inputs, results):
    """
    Construit un contexte RAG compact, structuré et optimisé pour Gemini.
    Ce contexte est utilisé pour :
    - générer une bio professionnelle courte (6 lignes max)
    - générer un plan d’apprentissage synthétique (10 lignes max)
    """

    # =====================================================
    # 1) SBERT – Scores & Profil
    # =====================================================
    percent_scores = {k: int(v * 100) for k, v in results["block_scores"].items()}
    job_reco = results["job_recommendation"]

    sorted_scores = sorted(percent_scores.items(), key=lambda x: x[1], reverse=True)

    strengths = ", ".join([f"{k} ({v}%)" for k, v in sorted_scores[:2]])
    weaknesses = ", ".join([f"{k} ({v}%)" for k, v in sorted_scores[-2:]])

    # =====================================================
    # 2) Informations utilisateur (compressées)
    # =====================================================
    projects = " | ".join([p.strip() for p in inputs["projects"] if p.strip()])
    tech_skills = ", ".join(inputs["tech_skills"]) if inputs["tech_skills"] else "Non renseigné"
    soft_skills = ", ".join(inputs["soft_skills"]) if inputs["soft_skills"] else "Non renseigné"

    likert_summary = ", ".join([f"{k}: {v}/5" for k, v in inputs["likert"].items()])

    # =====================================================
    # 3) CONTEXTE FINAL – Ultra lisible pour Gemini
    # =====================================================
    context = f"""
=== PROFIL UTILISATEUR (SYNTHÈSE) ===
Domaine d'intérêt : {inputs['domain_choice']}
Compétences techniques : {tech_skills}
Soft skills : {soft_skills}
Auto-évaluation : {likert_summary}
Projets réalisés : {projects}

=== ANALYSE SBERT ===
Scores par bloc (%) : {percent_scores}
Points forts : {strengths}
Points faibles : {weaknesses}
Métier recommandé : {job_reco}

=== INSTRUCTIONS IA ===
Tu es un expert RH & pédagogique.
Produis deux éléments : 
1) Une bio professionnelle courte (max 6 lignes), claire et valorisante.
2) Un plan d'apprentissage structuré : 
   - 3 objectifs
   - 3 recommandations concrètes
   - conclusion très courte (1–2 lignes)
Contraintes : 
- Style simple, fluide, professionnel
- Pas de répétitions
- Ne pas réécrire le contexte
"""

    return context.strip()
