# rag_engine.py — Moteur RAG MaghrebCyber
import os
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from groq import Groq

# Nom de la collection
COLLECTION_NAME = "maghrebcyber"

# Initialisation des clients
def init_clients():
    """Initialise et retourne les clients Qdrant, modèle et Groq"""
    
    qdrant = QdrantClient(
        url=os.environ["QDRANT_URL"],
        api_key=os.environ["QDRANT_API_KEY"]
    )
    
    model = SentenceTransformer("BAAI/bge-m3")
    
    groq_client = Groq(
        api_key=os.environ["GROQ_API_KEY"]
    )
    
    return qdrant, model, groq_client


def rechercher_chunks(question, qdrant, model, top_k=5):
    """Recherche les chunks les plus pertinents"""
    
    vecteur = model.encode(
        question,
        normalize_embeddings=True
    ).tolist()
    
    resultats = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=vecteur,
        limit=top_k,
        with_payload=True
    ).points
    
    return resultats


def generer_reponse(question, qdrant, model, groq_client, top_k=5):
    """Pipeline RAG complet — retourne réponse + sources + confiance"""
    
    # Recherche
    chunks = rechercher_chunks(question, qdrant, model, top_k)
    
    # Construction du contexte
    contexte = ""
    sources = []
    for i, chunk in enumerate(chunks):
        contexte += f"\n[Source {i+1}] {chunk.payload['text']}\n"
        sources.append({
            "fichier": chunk.payload['source'].replace("documents/", ""),
            "page": chunk.payload['page'] + 1,
            "score": round(chunk.score, 4)
        })
    
    # Prompt
    prompt = f"""Tu es MaghrebCyber, un assistant expert en cybersécurité \
spécialisé dans la réglementation marocaine et internationale.

Réponds à la question en te basant UNIQUEMENT sur le contexte fourni.
Si la réponse n'est pas dans le contexte, dis-le clairement.
Sois précis, cite les articles de loi quand c'est possible.
Réponds dans la même langue que la question.

CONTEXTE :
{contexte}

QUESTION : {question}

RÉPONSE :"""
    
    # Génération
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1000
    )
    
    reponse_texte = response.choices[0].message.content
    
    # Score de confiance
    score_moyen = sum(s['score'] for s in sources) / len(sources)
    if score_moyen >= 0.6:
        confiance = "🟢 Élevée"
    elif score_moyen >= 0.45:
        confiance = "🟡 Moyenne"
    else:
        confiance = "🔴 Faible"
    
    return {
        "reponse": reponse_texte,
        "sources": sources,
        "confiance": confiance,
        "score_moyen": round(score_moyen, 4)
    }
