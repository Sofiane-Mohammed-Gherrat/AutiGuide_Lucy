from autiguide.retrieval import retrieve_top_k   # whatever your existing TF-IDF lookup is called
import requests

LMSTUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL = "local-model"  # LM Studio ignores this if only one model is loaded, but harmless to set

SYSTEM_PROMPT = """You are Nurse Mode, part of AutiGuide, a support tool for caregivers 
of autistic children. Answer ONLY using the CONTEXT provided below. 
Do not add medical claims, therapies, or facts not present in the context. 
If the context does not answer the question, say you don't have information 
on that and suggest the caregiver consult a professional. 
Keep tone warm, brief, and practical."""

def build_prompt(message, context_entries):
    context_text = "\n\n".join(
        f"[{e['category']}] {e['response']['detailed']}" for e in context_entries
    )
    return [
        {"role": "system", "content": f"{SYSTEM_PROMPT}\n\nCONTEXT:\n{context_text}"},
        {"role": "user", "content": message},
    ]

def get_nurse_response(message, history=None):
    context_entries = retrieve_top_k(message, k=3)

    if not context_entries or context_entries[0]["score"] < 0.15:
        return {
            "answer": "I don't have solid information on that in my knowledge base. "
                      "It's best to check with a pediatrician or ASD specialist.",
            "sources": [],
        }

    messages = build_prompt(message, context_entries)
    if history:
        messages = messages[:1] + history + messages[1:]

    try:
        r = requests.post(LMSTUDIO_URL, json={
            "model": MODEL,
            "messages": messages,
            "temperature": 0.3,   # keep it low — you want grounded, not creative
            "stream": False,
        }, timeout=30)
        r.raise_for_status()
        reply = r.json()["choices"][0]["message"]["content"]
    except requests.exceptions.ConnectionError:
        return {
            "answer": "Nurse Mode is unavailable right now (local AI server not running). "
                      "Please try Retrieval Mode instead.",
            "sources": [],
        }

    return {
        "answer": reply,
        "sources": [e["category"] for e in context_entries],
        "when_to_seek_help": context_entries[0]["response"].get("when_to_seek_help"),
    }