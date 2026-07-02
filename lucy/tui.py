"""
AutiGuide TUI
-------------
A terminal mirror of the Streamlit app, for testing the chatbot pipeline
on Windows without needing Streamlit to run.

Requires: pip install rich prompt_toolkit

Run:
    python tui.py
"""

import json
from pathlib import Path

from rich.console import Console, Group
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.status import Status
from rich.text import Text
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import WordCompleter

#from .lm_chatbot import get_response
from .nurse_mode import get_nurse_response

# --------------------------------------------------
# Constants (mirrors Streamlit app)
# --------------------------------------------------

CONVERSATION_FILE = Path("conversation.json")
PROMPT_HISTORY_FILE = Path(".tui_prompt_history")

COMMANDS = {"/exit", "/quit", "/clear", "/history"}

USER_AVATAR = "✊"
BOT_AVATAR = "🧩"

PIPELINE_STEPS = [
    "Tokenization",
    "Stopword Removal",
    "Lemmatization",
    "TF-IDF",
    "Cosine Similarity",
]

KNOWLEDGE_BASE_CATEGORIES = [
    "Autism",
    "Communication",
    "Behaviour",
    "Sensory Processing",
    "Therapy",
    "Education",
]

console = Console()

# --------------------------------------------------
# Conversation persistence (self-contained, no st.session_state)
# --------------------------------------------------


def load_conversation():
    if CONVERSATION_FILE.exists():
        with open(CONVERSATION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_conversation(messages):
    with open(CONVERSATION_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)


def clear_conversation():
    if CONVERSATION_FILE.exists():
        CONVERSATION_FILE.unlink()
    return []


# --------------------------------------------------
# Sidebar-equivalent (printed once at startup)
# --------------------------------------------------


def print_sidebar():
    table = Table.grid(padding=(0, 2))
    table.add_column()
    table.add_column()

    pipeline_text = "\n".join(f"[green]✔[/green] {step}" for step in PIPELINE_STEPS)
    kb_text = "\n".join(f"[cyan]● {cat}[/cyan]" for cat in KNOWLEDGE_BASE_CATEGORIES)

    table.add_row(
        Panel(pipeline_text, title="Search Engine", border_style="green"),
        Panel(kb_text, title="Knowledge Base", border_style="cyan"),
    )

    console.print(
        Panel(
            "An offline autism information assistant using NLP and a local knowledge base.",
            title="🧩 AutiGuide",
            border_style="magenta",
        )
    )
    console.print(table)
    console.print(
        "[dim]Commands: type your question, /history to toggle the panel, "
        "/clear to reset, /exit to quit (Ctrl+C is disabled)[/dim]\n"
    )


# --------------------------------------------------
# Message rendering
# --------------------------------------------------


def render_history_panel(messages):
    """Build one Panel containing the full conversation."""
    if not messages:
        body = Text("No messages yet. Ask a question to get started.", style="dim italic")
        return Panel(body, title="🧩 Conversation", border_style="magenta")

    blocks = []
    for i, message in enumerate(messages):
        if message["role"] == "user":
            blocks.append(Text(f"{USER_AVATAR} You", style="bold blue"))
            blocks.append(Text(message["content"]))
        else:
            blocks.append(Text(f"{BOT_AVATAR} AutiGuide", style="bold green"))
            blocks.append(Markdown(message["content"]))

        if i < len(messages) - 1:
            blocks.append(Text(""))  # spacing between turns

    return Panel(Group(*blocks), title="🧩 Conversation", border_style="magenta")


def print_history(messages):
    console.print(render_history_panel(messages))


# --------------------------------------------------
# Main loop
# --------------------------------------------------


def render_latest_turn_panel(messages):
    """Show just the most recent user/assistant exchange."""
    if not messages:
        return None

    # Grab the last assistant message and the user message before it
    last = messages[-1]
    if last["role"] == "assistant" and len(messages) >= 2:
        turn = messages[-2:]
    else:
        turn = [last]

    blocks = []
    for i, message in enumerate(turn):
        if message["role"] == "user":
            blocks.append(Text(f"{USER_AVATAR} You", style="bold blue"))
            blocks.append(Text(message["content"]))
        else:
            blocks.append(Text(f"{BOT_AVATAR} AutiGuide", style="bold green"))
            blocks.append(Markdown(message["content"]))
        if i < len(turn) - 1:
            blocks.append(Text(""))

    return Panel(Group(*blocks), title="Latest", border_style="green")


def redraw(messages, show_history=True, session_start=0):
    console.clear()
    print_sidebar()
    console.print()  # spacing before panel/hint
    if show_history:
        print_history(messages)
    else:
        console.print("[dim]Conversation panel hidden — type /history to show it.[/dim]")
        console.print()
        if len(messages) > session_start:
            latest = render_latest_turn_panel(messages)
            if latest is not None:
                console.print(latest)
    console.print()  # spacing after panel/hint


completer = WordCompleter(sorted(COMMANDS), ignore_case=True, sentence=True)
prompt_session = PromptSession(
    history=FileHistory(str(PROMPT_HISTORY_FILE)),
    completer=completer,
    complete_while_typing=True,
)


def ask_question():
    console.print(
        Panel(
            Text("Ask a question about autism...", style="italic dim"),
            title=f"{USER_AVATAR} You",
            border_style="blue",
        )
    )
    return prompt_session.prompt("> ")


def main():
    messages = load_conversation()
    session_start = len(messages)  # turns before this point belong to a prior run
    show_history = False
    redraw(messages, show_history, session_start)

    while True:
        try:
            prompt = ask_question()
        except KeyboardInterrupt:
            console.print("\n[dim]Ctrl+C is disabled here — type /exit to quit.[/dim]")
            continue
        except EOFError:
            console.print("\n[dim]Exiting.[/dim]")
            break

        text = prompt.strip()

        if not text:
            continue

        if text.startswith("/"):
            command = text.lower()

            if command not in COMMANDS:
                console.print(f"[red]Command unavailable:[/red] {text}")
                continue

            if command in ("/exit", "/quit"):
                break

            if command == "/clear":
                messages = clear_conversation()
                session_start = 0
                redraw(messages, show_history, session_start)
                console.print("[yellow]Conversation cleared.[/yellow]")
                continue

            if command == "/history":
                show_history = not show_history
                redraw(messages, show_history, session_start)
                continue

        try:
            messages.append({"role": "user", "content": text})
            save_conversation(messages)

            with Status("Searching knowledge base...", console=console, spinner="dots"):
                reply = get_nurse_response(text)["answer"]

            messages.append({"role": "assistant", "content": reply})
            save_conversation(messages)

            redraw(messages, show_history, session_start)
        except KeyboardInterrupt:
            console.print("\n[dim]Ctrl+C is disabled here — type /exit to quit.[/dim]")
            continue


if __name__ == "__main__":
    main()