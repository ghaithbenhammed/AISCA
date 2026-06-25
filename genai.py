import time
import streamlit as st
from google import genai

# ======================================================
# INITIALISATION GEMINI
# ======================================================

API_KEY = ""

client = genai.Client(api_key=API_KEY)

PRIMARY_MODEL = "gemini-2.5-flash"
FALLBACK_MODEL = "gemini-2.5-flash-lite"

# ======================================================
# APPEL GEMINI
# ======================================================

def call_gemini(prompt):

    models = [PRIMARY_MODEL, FALLBACK_MODEL]

    last_error = ""

    for model in models:

        wait = 2

        for attempt in range(5):

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                if hasattr(response, "text") and response.text:
                    return response.text.strip()

            except Exception as e:

                last_error = str(e)

                print("=" * 70)
                print(f"MODELE : {model}")
                print(f"Tentative : {attempt+1}/5")
                print(last_error)
                print("=" * 70)

                # quota / surcharge
                if (
                    "503" in last_error
                    or "429" in last_error
                    or "UNAVAILABLE" in last_error
                    or "RESOURCE_EXHAUSTED" in last_error
                ):

                    time.sleep(wait)
                    wait *= 2
                    continue

                break

    print(last_error)

    return """
⚠️ L'IA Gemini est momentanément indisponible.

Les résultats SBERT restent valides.

Réessayez dans quelques minutes.
"""


# ======================================================
# BIO
# ======================================================

@st.cache_data(show_spinner=False)
def generate_bio(context):

    prompt = f"""
Tu es un expert RH.

Analyse ce profil :

{context}

Rédige uniquement une bio professionnelle.

Contraintes :

- 5 lignes maximum
- style professionnel
- pas de listes
- pas de répétitions
- pas d'introduction
"""

    return call_gemini(prompt)


# ======================================================
# PLAN
# ======================================================

@st.cache_data(show_spinner=False)
def generate_learning_plan(context):

    prompt = f"""
Tu es un coach Data & IA.

Analyse ce profil :

{context}

Génère uniquement un plan d'apprentissage.

Format :

Objectifs
- ...
- ...
- ...

Recommandations
- ...
- ...
- ...

Conclusion
2 lignes maximum.

Maximum 10 lignes.
"""

    return call_gemini(prompt)