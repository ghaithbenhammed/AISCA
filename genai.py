import streamlit as st
from google import genai
import time

# ======================================================
# 🔐 INITIALISATION CLIENT GOOGLE GEMINI
# ======================================================
client = genai.Client(api_key="AIzaSyAVhwxjzD9QHnlbOl9_vsvAnTcedsOTgKY")

PRIMARY_MODEL = "gemini-2.5-flash"   # modèle demandé par la prof
FALLBACK_MODEL = "gemini-pro"        # modèle stable si Flash plante


# ======================================================
# 🔄 FONCTION GÉNÉRIQUE AVEC RETRY + FALLBACK
# ======================================================
def call_gemini(prompt, max_retries=3):
    """
    Appelle Gemini 2.5 Flash avec gestion :
    - surcharge (503)
    - quota dépassé (429)
    - retry automatique
    - fallback vers Gemini-Pro
    """

    # 1) Tentatives avec Gemini 2.5 Flash
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=PRIMARY_MODEL,
                contents=prompt
            )
            return response.text

        except Exception as e:
            err = str(e)

            # Si modèle saturé (503)
            if "503" in err or "overloaded" in err:
                print(f"[Gemini Flash] Surcharge (503). Tentative {attempt+1}/{max_retries}…")
                time.sleep(1.2)
                continue

            # Si quota dépassé (429)
            if "429" in err:
                print("[Gemini Flash] QUOTA dépassé. Bascule automatique vers Gemini Pro.")
                break

            # Erreur inattendue → on sort
            print("[Gemini Flash] Erreur inconnue :", err)
            break

    # 2) Fallback automatique → Gemini Pro
    try:
        print("[Fallback] Passage vers Gemini Pro…")
        response = client.models.generate_content(
            model=FALLBACK_MODEL,
            contents=prompt
        )
        return response.text

    except Exception as e:
        print("[Gemini Pro] Erreur :", e)
        return "⚠️ Impossible de générer l'analyse IA pour le moment. Réessayez plus tard."


# ======================================================
# 🧠 BIO PROFESSIONNELLE (avec cache)
# ======================================================
@st.cache_data(show_spinner=False)
def generate_bio(context):
    prompt = f"""
Génère une bio professionnelle courte (5 à 6 lignes) basée sur ce profil :

{context}

Contraintes :
- phrases courtes et claires
- ton professionnel mais simple
- pas de répétitions
- maximum 6 lignes
"""
    return call_gemini(prompt)


# ======================================================
# 🎯 PLAN D'APPRENTISSAGE (avec cache)
# ======================================================
@st.cache_data(show_spinner=False)
def generate_learning_plan(context):
    prompt = f"""
Génère un plan d'apprentissage très synthétique basé sur ce profil :

{context}

Format attendu :
- 3 objectifs clairs
- 3 recommandations concrètes
- conclusion motivante (1 à 2 lignes)
- maximum 10 lignes au total
"""
    return call_gemini(prompt)
