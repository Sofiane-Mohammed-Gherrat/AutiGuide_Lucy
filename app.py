# --------------------------------------------------
# AutiGuide - Flask entry point
# --------------------------------------------------
#
# This file only creates the Flask app, applies configuration, and
# defines the HTTP routes. All chatbot logic lives in the autiguide/
# package (see autiguide/__init__.py for a map of the modules).

from flask import Flask, jsonify, render_template, request, session

from autiguide import config
from autiguide.categories import DEFAULT_SUGGESTIONS
from autiguide.chatbot import get_autiguide_response
from autiguide.responses import build_response
from knowledge_base import knowledge_base

from lucy.nurse_mode import get_nurse_response

#create the Flask web application
app = Flask(__name__)

#apply the secret key, cookie and request-size settings
config.apply_to(app)


#show the chatbot webpage
@app.route("/", methods=["GET"])
def home():
    #load templates/index.html
    return render_template("index.html")

@app.route("/nurse")
def nurse():
    return render_template("nurse.html")


#receive one user message and return one chatbot response
@app.route("/chat", methods=["POST"])
def chat():
    #read the JSON object sent by the HTML page
    data = request.get_json(silent=True)

    #use an empty dictionary when the request does not contain valid JSON
    if data is None:
        data = {}

    #get the user message from the JSON object
    message = data.get("message", "")

    #reject missing or non-text messages
    if not isinstance(message, str) or not message.strip():
        response = build_response(
            "Input Validation",
            "Please type a question.",
            suggestions=DEFAULT_SUGGESTIONS,
            confidence="none",
        )
        return jsonify(response), 400

    #reject messages longer than the interface limit
    if len(message) > config.MAX_MESSAGE_LENGTH:
        response = build_response(
            "Input Validation",
            f"Please shorten the message to {config.MAX_MESSAGE_LENGTH} characters or fewer.",
            suggestions=DEFAULT_SUGGESTIONS,
            confidence="none",
        )
        return jsonify(response), 400

    #remove extra spaces and pass the message to the chatbot logic
    response = get_autiguide_response(message.strip())

    #return the chatbot dictionary as JSON
    return jsonify(response)


#clear the conversation memory and active guided flow
@app.route("/reset", methods=["POST"])
def reset():
    #remove all saved session values
    session.clear()

    #confirm that the reset was completed
    return jsonify({"status": "reset"})


#return simple information used to check that the server is working
@app.route("/health", methods=["GET"])
def health():
    #create a set so each category appears only once
    categories = {item["category"] for item in knowledge_base}

    #return the server status and knowledge base size
    return jsonify({
        "status": "ok",
        "type": "retrieval-based with rule-based safety",
        "knowledge_base_items": len(knowledge_base),
        "categories": sorted(categories),
    })

@app.route("/nurse_chat", methods=["POST"])
def nurse_chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")

    if not isinstance(message, str) or not message.strip():
        return jsonify({"answer": "Please type a question.", "grounded": False}), 400

    if len(message) > config.MAX_MESSAGE_LENGTH:
        return jsonify({
            "answer": f"Please shorten the message to {config.MAX_MESSAGE_LENGTH} characters or fewer.",
            "grounded": False,
        }), 400

    history = session.get("nurse_history", [])
    result = get_nurse_response(message.strip(), history=history)

    history.append({"role": "user", "content": message.strip()})
    history.append({"role": "assistant", "content": result["answer"]})
    session["nurse_history"] = history[-10:]  # keep last 10 turns

    return jsonify(result)


#run the Flask development server when app.py is opened directly
if __name__ == "__main__":
    #debug mode is useful during the student project demonstration
    app.run(host="127.0.0.1", port=5000, debug=True)
