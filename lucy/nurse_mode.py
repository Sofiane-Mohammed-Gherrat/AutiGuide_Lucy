import requests
from .lm_chatbot import get_response, FALLBACK
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

LMSTUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL = "local-model"

SYSTEM_PROMPT = (
    "You are Nurse Mode, part of AutiGuide, a support tool for caregivers "
    "of autistic children. You will be given a structured analysis (in markdown) "
    "produced by a knowledge-base retrieval system. Rewrite it as a warm, natural, "
    "conversational reply to the caregiver. Do NOT add any medical claim, fact, or "
    "suggestion that isn't already present in the analysis. If the analysis says "
    "no information was found, say so plainly and suggest consulting a professional. "
    "Keep it concise and practical."
)


def get_nurse_response(question: str, history: list | None = None) -> dict:
    kb_markdown = get_response(question)

    # No point calling the LLM to "rephrase" a plain fallback message
    if kb_markdown.strip() == FALLBACK.strip():
        return {"answer": FALLBACK, "grounded": False}

    messages = [
        {"role": "system", "content": f"{SYSTEM_PROMPT}\n\nANALYSIS:\n{kb_markdown}"}
    ]
    if history:
        messages += history
    messages.append({"role": "user", "content": question})

    try:
        r = requests.post(LMSTUDIO_URL, json={
            "model": MODEL,
            "messages": messages,
            "temperature": 0.3,
            "stream": False,
        }, timeout=30)
        r.raise_for_status()
        reply = r.json()["choices"][0]["message"]["content"]
    except requests.exceptions.ConnectionError:
        # LLM unreachable — fall back to the raw retrieval answer, not a dead end
        return {"answer": kb_markdown, "grounded": True, "llm_used": False}

    return {"answer": reply, "grounded": True, "llm_used": True}


if __name__ == "__main__":
    console = Console()
    question = "what is a meltdown? and what to do during a meltdown?"
    print("\n--- Running Nurse Mode Response ---")
    markdown_answer = get_nurse_response(question)["answer"]
    console.print(
        Panel(Markdown(markdown_answer), title="🧩 Answer", border_style="magenta")
    )