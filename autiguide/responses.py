# --------------------------------------------------
# Shared response builder
# --------------------------------------------------
#
# Every part of the chatbot (safety rules, guided flows, general
# conversation, knowledge base retrieval) returns its answer through
# this one function, so the frontend always receives the same shape
# of JSON object.

from flask import session


#create one standard response dictionary for the frontend
def build_response(
    category,
    answer,
    risk="low",
    steps=None,
    suggestions=None,
    source="AutiGuide rule",
    confidence="rule-based",
    item=None,
):
    #use empty lists when steps or suggestions are missing
    if steps is None:
        steps = []

    if suggestions is None:
        suggestions = []

    #create the main response sent to the HTML page
    response = {
        "category": category,
        "risk_level": risk,
        "answer": answer,
        "steps": steps,
        "suggestions": suggestions,
        "source_type": source,
        "confidence": confidence,
    }

    #add source details and conversation memory for knowledge base answers
    if item is not None:
        response["item_id"] = item["id"]
        response["source_url"] = item["source_url"]
        response["last_reviewed"] = item["last_reviewed"]

        #remember the last item so the user can ask to continue
        session["last_item_id"] = item["id"]
        session["last_category"] = item["category"]

    #return the completed response
    return response
