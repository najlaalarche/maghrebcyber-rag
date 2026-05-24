# app.py — Interface Streamlit MaghrebCyber RAG
import streamlit as st
import os
from rag_engine import init_clients, generer_reponse

# Configuration de la page
st.set_page_config(
    page_title="MaghrebCyber RAG",
    page_icon="🛡️",
    layout="wide"
)

# Initialisation des clients (une seule fois)
@st.cache_resource
def charger_clients():
    return init_clients()

qdrant, model, groq_client = charger_clients()

# ─── SIDEBAR ───────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/2/2c/Flag_of_Morocco.svg", width=80)
    st.title("🛡️ MaghrebCyber RAG")
    st.markdown("Assistant intelligent en cybersécurité marocaine")
    st.divider()
    
    st.markdown("### 📚 Documents indexés")
    docs = [
        "Loi 05-20 Cybersécurité",
        "Loi 09-08 Données personnelles",
        "Stratégie Nationale Cyber 2030",
        "DNSSI",
        "Rapport annuel maCERT",
        "Convention de Budapest",
        "Guide homologation SI",
        "Référentiel audit SI",
        "Référentiel vérification appli"
    ]
    for doc in docs:
        st.markdown(f"- {doc}")
    
    st.divider()
    st.markdown("### ⚙️ Paramètres")
    top_k = st.slider("Nombre de sources", 3, 8, 5)
    
    st.divider()
    st.markdown("### 🌍 Langues supportées")
    st.markdown("🇫🇷 Français &nbsp;&nbsp; 🇲🇦 Arabe")
    
    st.divider()
    st.caption("Développé par Najlâa Larche — ESITH 2025")

# ─── HEADER ────────────────────────────────────────────────
st.title("🛡️ MaghrebCyber RAG")
st.markdown("**Assistant de veille réglementaire en cybersécurité — Maroc & International**")
st.divider()

# ─── MÉMOIRE DE CONVERSATION ───────────────────────────────
if "historique" not in st.session_state:
    st.session_state.historique = []

# ─── AFFICHAGE DE L'HISTORIQUE ─────────────────────────────
for message in st.session_state.historique:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    else:
        with st.chat_message("assistant", avatar="🛡️"):
            st.write(message["content"])
            if "sources" in message:
                with st.expander("📚 Sources utilisées"):
                    for i, source in enumerate(message["sources"]):
                        st.markdown(
                            f"**{i+1}.** `{source['fichier']}` "
                            f"— page {source['page']} "
                            f"*(score: {source['score']})*"
                        )
                st.caption(
                    f"📊 Confiance : {message['confiance']} "
                    f"| Score moyen : {message['score_moyen']}"
                )

# ─── INPUT UTILISATEUR ─────────────────────────────────────
question = st.chat_input(
    "Posez votre question en français أو بالعربية..."
)

if question:
    # Afficher la question
    with st.chat_message("user"):
        st.write(question)
    
    # Ajouter à l'historique
    st.session_state.historique.append({
        "role": "user",
        "content": question
    })
    
    # Générer la réponse
    with st.chat_message("assistant", avatar="🛡️"):
        with st.spinner("🔍 Recherche dans les documents..."):
            resultat = generer_reponse(
                question, qdrant, model, groq_client, top_k
            )
        
        # Afficher la réponse
        st.write(resultat["reponse"])
        
        # Afficher les sources
        with st.expander("📚 Sources utilisées"):
            for i, source in enumerate(resultat["sources"]):
                st.markdown(
                    f"**{i+1}.** `{source['fichier']}` "
                    f"— page {source['page']} "
                    f"*(score: {source['score']})*"
                )
        
        # Afficher la confiance
        st.caption(
            f"📊 Confiance : {resultat['confiance']} "
            f"| Score moyen : {resultat['score_moyen']}"
        )
    
    # Sauvegarder dans l'historique
    st.session_state.historique.append({
        "role": "assistant",
        "content": resultat["reponse"],
        "sources": resultat["sources"],
        "confiance": resultat["confiance"],
        "score_moyen": resultat["score_moyen"]
    })
