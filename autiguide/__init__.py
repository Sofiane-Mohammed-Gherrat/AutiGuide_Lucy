# --------------------------------------------------
# AutiGuide chatbot package
# --------------------------------------------------
#
# This package holds the chatbot's logic, split into focused modules:
#
#   text_processing.py  - lowercase/clean text, stopwords, synonyms, stemming
#   categories.py        - topic keyword lists and category detection
#   responses.py          - the shared response dictionary builder
#   retrieval.py           - knowledge base search, scoring and fallback
#   safety.py               - rule-based safety checks (run first, always)
#   guided_flows.py          - the five step-by-step guided support tools
#   conversation.py           - greetings, help, thanks and follow-ups
#   chatbot.py                  - top-level decision function (get_autiguide_response)
#
# app.py at the project root only creates the Flask app, wires up
# config, and defines the HTTP routes; it delegates all chatbot logic
# to this package.
