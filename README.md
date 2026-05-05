# Agent d’analyse documentaire (local)

Petit projet d’agent IA qui permet d’analyser un document texte avec Llama 3 en local (via Ollama).

---

## Ce que fait l’agent

Tu charges un document, puis tu peux lui poser des questions comme si tu parlais à ChatGPT.

Il peut :

- Résumer le document
- Extraire des informations (dates, personnes, chiffres…)
- Répondre à des questions précises
- Comparer des parties du document

L’agent choisit automatiquement quoi faire (il peut utiliser des "tools" en interne).

---

## Comment ça marche

1. Tu poses une question
2. Le modèle décide :
   - soit répondre directement
   - soit appeler un tool (résumé, extraction…)
3. Si un tool est utilisé → résultat récupéré
4. Le modèle reformule une réponse propre

---

##  Structure

Agent.py
Tout est dans un seul fichier :

- appel au modèle (Ollama)
- tools
- boucle agentique
- interface terminal

---
##  Exemples de questions :
"Compare l'adoption de l'IA en France et en Allemagne"
"Quels sont les nouveaux métiers créés par l'IA ?"
"Extrais tous les chiffres mentionnés dans ce rapport"

##  Installation

### 1. Installer Ollama
https://ollama.com

### 2. Télécharger le modèle
```bash
ollama pull llama3
