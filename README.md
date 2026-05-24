markdown# 🛡️ MaghrebCyber RAG

> Assistant intelligent de veille réglementaire en cybersécurité marocaine et internationale, multilingue français/arabe, basé sur une architecture RAG (Retrieval Augmented Generation).

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?logo=streamlit)
![Qdrant](https://img.shields.io/badge/Qdrant-Cloud-purple)
![Groq](https://img.shields.io/badge/Groq-Llama_3.3_70B-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 Présentation

MaghrebCyber RAG est un assistant conversationnel capable de répondre à des questions complexes sur la **réglementation cybersécurité au Maroc et à l'international**, en se basant exclusivement sur des documents officiels indexés.

Contrairement à un LLM classique qui répond de mémoire (et peut halluciner), MaghrebCyber RAG **ancre chaque réponse dans des textes juridiques réels**, cite ses sources avec numéros de page, et indique un score de confiance.

### Fonctionnalités clés

- 🔍 **Recherche sémantique** — retrouve les passages pertinents même sans correspondance exacte de mots
- 🌍 **Multilingue FR/AR** — pose ta question en français ou en arabe, la réponse suit automatiquement
- 📚 **Sources citées** — chaque réponse indique le document source et le numéro de page
- 📊 **Score de confiance** — indicateur de fiabilité basé sur la similarité cosinus
- 💬 **Mémoire de conversation** — l'assistant se souvient du contexte de la discussion
- ⚖️ **Anti-hallucination** — répond uniquement à partir du contexte fourni

---

## 🏗️ Architecture
Question utilisateur
↓
Embedding bge-m3 (1024 dim)
↓
Recherche Qdrant Cloud (similarité cosinus)
↓
Top-5 chunks pertinents
↓
Construction du prompt (question + contexte)
↓
Génération Groq / Llama 3.3 70B
↓
Réponse + sources + score de confiance

---

## 📚 Documents indexés

| Document | Source | Langue |
|---|---|---|
| Loi n° 05-20 relative à la cybersécurité | DGSSI / Maroc | Français |
| Loi n° 09-08 protection des données personnelles | CNDP / Maroc | Français |
| Stratégie Nationale de Cybersécurité 2030 | DGSSI / Maroc | Français |
| Directive Nationale SSI (DNSSI) | DGSSI / Maroc | Français |
| Rapport annuel maCERT | maCERT / Maroc | Français |
| Convention de Budapest sur la cybercriminalité | Conseil de l'Europe | Français |
| Guide d'homologation des SI sensibles | DGSSI / Maroc | Français |
| Référentiel de qualification des auditeurs SI | DGSSI / Maroc | Français |
| Référentiel de vérification de la sécurité des applis | DGSSI / Maroc | Français |

**Total : 9 documents — 314 pages — 1624 chunks indexés**

---

## 🛠️ Stack technique

| Composant | Technologie | Rôle |
|---|---|---|
| Embeddings | BAAI/bge-m3 | Transformation texte → vecteurs 1024 dim |
| Base vectorielle | Qdrant Cloud | Stockage et recherche de vecteurs |
| LLM | Groq / Llama 3.3 70B | Génération de réponses |
| Interface | Streamlit | Application web |
| Versioning | GitHub | Gestion du code |
| Déploiement | Streamlit Community Cloud | Hébergement public |

---

## 🚀 Lancer le projet en local

### Prérequis
- Python 3.10+
- Compte Qdrant Cloud (gratuit)
- Clé API Groq (gratuite)

### Installation

```bash
# Cloner le repo
git clone https://github.com/najlaalarche/maghrebcyber-rag.git
cd maghrebcyber-rag

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec tes clés API
```

### Configuration `.env`

```env
GROQ_API_KEY=gsk_xxxx
QDRANT_URL=https://xxxx.eu-central-1-0.aws.cloud.qdrant.io
QDRANT_API_KEY=xxxx
```

### Lancement

```bash
streamlit run app.py
```

---

## 📁 Structure du projet
maghrebcyber-rag/
├── app.py                  # Interface Streamlit
├── rag_engine.py           # Moteur RAG (recherche + génération)
├── requirements.txt        # Dépendances Python
├── .env.example            # Template variables d'environnement
├── .gitignore              # Fichiers exclus du versioning
└── README.md               # Documentation

---

## 💡 Exemples de questions

**En français :**
- *"Quelles sont les obligations d'une entreprise selon la loi 05-20 ?"*
- *"Quels sont les pouvoirs de la CNDP en matière de contrôle ?"*
- *"Comment la DNSSI définit-elle un incident de sécurité critique ?"*

**En arabe :**
- *"ما هي العقوبات المقررة في حالة خرق البيانات الشخصية ؟"*
- *"ما هي مهام الدير الوطني لأمن المعلومات ؟"*

---

## 🔮 Perspectives d'évolution

- [ ] Support de la darija via fine-tuning
- [ ] Mode comparaison Maroc vs UE (NIS2, RGPD)
- [ ] Ajout de nouveaux documents (rapports ANSSI, directives africaines)
- [ ] Export PDF des réponses
- [ ] API REST pour intégration externe

---

## 👩‍💻 Auteur

**Najlâa Larche**
Étudiante ingénieure — ESITH Casablanca
Présidente Club Cybotics

[![GitHub](https://img.shields.io/badge/GitHub-najlaalarche-black?logo=github)](https://github.com/najlaalarche)

---

## 📄 Licence

Ce projet est sous licence MIT — voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

*Projet réalisé dans le cadre du TP2 RAG — 2025*
