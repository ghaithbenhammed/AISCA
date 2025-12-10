from google import genai

# Initialisation du client Gemini (Nouveau SDK)
client = genai.Client(api_key="AIzaSyCHnGbSQOU-mTRYGs1vFbHPlULDJYh-gac")


def generate_bio(context):
    prompt = f"""
Produis une bio professionnelle très courte (4 à 6 lignes) basée sur ce profil :

{context}

Contraintes :
- phrases courtes
- ton professionnel mais simple
- pas de détails inutiles
- pas plus de 6 lignes
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def generate_learning_plan(context):
    prompt = f"""
Produis un plan d'apprentissage concis basé sur ce profil :

{context}

Format demandé :
- 3 objectifs courts
- 3 recommandations concrètes
- une conclusion motivante (max 2 lignes)
Réponse très courte et synthétique (max 10 lignes).
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text
