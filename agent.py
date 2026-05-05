"""
Agent d'analyse documentaire (version simple, local avec Llama 3)

Objectif :
- Lire un document
- Permettre à l'utilisateur de poser des questions
- Utiliser des "tools" si nécessaire (résumé, extraction, etc.)
"""

import json
import requests


# ─────────────────────────────────────────────
# Appel au modèle local (Ollama)
# ─────────────────────────────────────────────

def call_llm(prompt: str) -> str:
    """Envoie un prompt au modèle Llama 3 via Ollama"""
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]


# ─────────────────────────────────────────────
# Tools (fonctions que l'agent peut utiliser)
# ─────────────────────────────────────────────

def summarize(document: str, length: str) -> str:
    return call_llm(f"{document}\n\nTâche : fais un résumé {length}.")


def extract_entities(document: str, entity_types: list) -> str:
    return call_llm(f"{document}\n\nTâche : extrais les entités suivantes : {entity_types}.")


def answer_question(document: str, question: str) -> str:
    return call_llm(f"{document}\n\nTâche : réponds à la question suivante uniquement avec le document : {question}")


def compare_sections(document: str, a: str, b: str) -> str:
    return call_llm(f"{document}\n\nTâche : compare '{a}' et '{b}' dans le document.")


# ─────────────────────────────────────────────
# Exécution d’un tool
# ─────────────────────────────────────────────

def execute_tool(name, params, document):
    print(f"→ Utilisation du tool : {name}")

    if name == "summarize":
        return summarize(document, params["length"])

    if name == "extract_entities":
        return extract_entities(document, params["entity_types"])

    if name == "answer_question":
        return answer_question(document, params["question"])

    if name == "compare_sections":
        return compare_sections(document, params["aspect_a"], params["aspect_b"])

    return "Tool inconnu"


# ─────────────────────────────────────────────
# Boucle agentique simplifiée
# ─────────────────────────────────────────────

def run_agent(user_input, document):
    """
    1. On envoie la question au modèle
    2. Il décide s’il appelle un tool (via JSON)
    3. Si oui → on exécute le tool
    4. Puis on génère la réponse finale
    """

    system_prompt = """
Tu es un agent qui analyse des documents.

Tu peux utiliser ces outils :
- summarize
- extract_entities
- answer_question
- compare_sections

Si un outil est nécessaire, réponds UNIQUEMENT en JSON :
{"tool": "...", "input": {...}}

Sinon, réponds normalement.
"""

    prompt = f"""
SYSTEM:
{system_prompt}

DOCUMENT:
{document}

QUESTION:
{user_input}
"""

    response = call_llm(prompt)

    # Essayer de voir si le modèle veut utiliser un tool
    try:
        data = json.loads(response)

        if "tool" in data:
            result = execute_tool(data["tool"], data["input"], document)

            # deuxième appel pour reformuler proprement la réponse
            final_prompt = f"""
DOCUMENT:
{document}

QUESTION:
{user_input}

RÉSULTAT INTERMÉDIAIRE:
{result}

Donne une réponse finale claire et structurée.
"""
            return call_llm(final_prompt)

    except:
        # Si ce n'est pas du JSON → réponse directe
        pass

    return response


# ─────────────────────────────────────────────
# Chargement du document
# ─────────────────────────────────────────────

def load_document(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ─────────────────────────────────────────────
# Interface CLI
# ─────────────────────────────────────────────

def main():
    print("=== Agent d'analyse documentaire (local) ===")

    path = input("Chemin du document : ")
    document = load_document(path)

    print("\nAgent prêt. Pose tes questions (quit pour sortir)\n")

    while True:
        question = input("Toi : ")

        if question.lower() in ["quit", "exit"]:
            break

        print("\nAgent :")
        print(run_agent(question, document))
        print()


if __name__ == "__main__":
    main()