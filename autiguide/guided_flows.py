# --------------------------------------------------
# Guided support flows
# --------------------------------------------------
#
# A guided flow walks the caregiver through a short set of
# multiple-choice questions (stored in the session) and then returns
# tailored advice once the last question is answered.

from flask import session

from autiguide.categories import DEFAULT_SUGGESTIONS
from autiguide.responses import build_response
from autiguide.text_processing import clean_text, contains_any_phrase


#store the questions and buttons used by the five guided support tools
GUIDED_FLOWS = {
    "meltdown": {
        "title": "Meltdown Support Guide",
        "start_phrases": ["start meltdown guide", "meltdown guide"],
        "questions": [
            {
                "key": "safe",
                "question": "Is the child physically safe right now?",
                "options": ["Yes, safe", "No, there is danger", "I am not sure"],
            },
            {
                "key": "trigger",
                "question": "What seems to be the main trigger?",
                "options": [
                    "Noise or crowd",
                    "Change in routine",
                    "Tired, hungry or in pain",
                    "Unknown",
                ],
            },
            {
                "key": "place",
                "question": "Where is this happening?",
                "options": ["Home", "School", "Public place"],
            },
        ],
    },
    "aggression": {
        "title": "Aggression Support Guide",
        "start_phrases": ["start aggression guide", "aggression guide"],
        "questions": [
            {
                "key": "injury",
                "question": "Is anyone injured or in immediate danger?",
                "options": ["Yes", "No", "I am not sure"],
            },
            {
                "key": "trigger",
                "question": "What happened immediately before the behaviour?",
                "options": [
                    "Demand or denied request",
                    "Sensory issue",
                    "Transition",
                    "Unknown",
                ],
            },
            {
                "key": "place",
                "question": "Where did it happen?",
                "options": ["Home", "School", "Public place"],
            },
        ],
    },
    "picky": {
        "title": "Picky Eating Guide",
        "start_phrases": ["start picky eating guide", "picky eating guide"],
        "questions": [
            {
                "key": "health",
                "question": "Is there weight loss, dehydration, weakness or persistent vomiting?",
                "options": ["Yes", "No", "I am not sure"],
            },
            {
                "key": "issue",
                "question": "What seems to be the main difficulty?",
                "options": [
                    "Texture",
                    "Smell or appearance",
                    "Very few accepted foods",
                    "Unknown",
                ],
            },
        ],
    },
    "school": {
        "title": "School Support Guide",
        "start_phrases": ["start school support guide", "school support guide"],
        "questions": [
            {
                "key": "issue",
                "question": "What is the main school concern?",
                "options": [
                    "Behaviour",
                    "Learning",
                    "Teacher communication",
                    "Friendships",
                ],
            },
            {
                "key": "trigger",
                "question": "Is there a known trigger?",
                "options": ["Noise", "Transitions", "Classwork", "Unknown"],
            },
        ],
    },
    "resources": {
        "title": "Malaysia Resource Guide",
        "start_phrases": [
            "start resource guide",
            "resource guide",
            "malaysia resource guide",
        ],
        "questions": [
            {
                "key": "need",
                "question": "What kind of support are you looking for?",
                "options": [
                    "Assessment",
                    "Therapy",
                    "School support",
                    "JKM or welfare",
                ],
            },
            {
                "key": "access",
                "question": "What is the main access issue?",
                "options": ["Cost", "Distance", "Waiting time", "Not sure"],
            },
        ],
    },
}


#return the current question of an active guided flow
def get_flow_question(flow_name):
    #get the selected flow and the saved session state
    flow = GUIDED_FLOWS[flow_name]
    flow_state = session["flow"]

    #get the current question using the saved step number
    current_question = flow["questions"][flow_state["step"]]

    #return the question and its option buttons
    return build_response(
        flow["title"],
        current_question["question"],
        risk="guided",
        suggestions=current_question["options"] + ["Cancel guide"],
        source="Guided rule-based support",
    )


#start one guided flow and save its first step in the session
def start_flow(flow_name):
    #save the flow name, current step and answers
    session["flow"] = {
        "name": flow_name,
        "step": 0,
        "answers": {},
    }

    #show the first question
    return get_flow_question(flow_name)


#return the final prepared advice after all flow questions are answered
def finish_flow(flow_name, answers):
    #remove the completed flow from the session
    session.pop("flow", None)

    #finish the meltdown guide
    if flow_name == "meltdown":
        #return urgent guidance when the child is not confirmed safe
        if answers.get("safe") != "Yes, safe":
            return build_response(
                "Meltdown Support Guide",
                "Safety comes first. Move away from immediate danger if you can do so safely. "
                "Call 999 when there is immediate danger or serious injury.",
                risk="high",
                steps=[
                    "Reduce noise, light and talking.",
                    "Give safe space.",
                    "Seek professional help if episodes are dangerous or frequent.",
                ],
                suggestions=[
                    "How can I prevent meltdowns?",
                    "What is sensory overload?",
                ],
            )

        #return normal meltdown recovery guidance
        return build_response(
            "Meltdown Support Guide",
            "The child is reported safe. Reduce demands and stimulation, allow time to recover "
            "and record the likely trigger so the plan can be improved.",
            risk="guided",
            steps=[
                "Use a calm, short voice.",
                "Move to a quieter place if possible.",
                "Avoid punishment and forced eye contact.",
                "Review the trigger after recovery.",
            ],
            suggestions=[
                "How can I prevent meltdowns?",
                "What is sensory overload?",
            ],
        )

    #finish the aggression guide
    if flow_name == "aggression":
        #return higher-risk guidance when injury or danger is possible
        if answers.get("injury") != "No":
            return build_response(
                "Aggression Support Guide",
                "Separate people from danger and check for injury. Use 999 for immediate serious "
                "danger. Arrange professional support when aggression is repeated or causes harm.",
                risk="high",
                suggestions=[
                    "How can I identify behaviour triggers?",
                    "How can I talk to the teacher?",
                ],
            )

        #return prevention guidance when nobody was injured
        return build_response(
            "Aggression Support Guide",
            "Use a calm, consistent response and investigate what happened before the behaviour. "
            "The trigger information can guide a shared prevention plan.",
            risk="guided",
            steps=[
                "Reduce talking until calm.",
                "Record the trigger and consequence.",
                "Teach a safe way to request help or a break.",
                "Use the same plan at home and school.",
            ],
            suggestions=[
                "How can I identify behaviour triggers?",
                "How can I talk to the teacher?",
            ],
        )

    #finish the picky eating guide
    if flow_name == "picky":
        #return a health warning when serious symptoms may be present
        if answers.get("health") != "No":
            return build_response(
                "Picky Eating Guide",
                "Weight loss, dehydration, weakness or persistent vomiting requires prompt "
                "professional medical assessment.",
                risk="high",
                suggestions=[
                    "When is food refusal serious?",
                    "Does diet cure autism?",
                ],
            )

        #return normal food introduction guidance
        return build_response(
            "Picky Eating Guide",
            "Keep accepted foods available and introduce change slowly without force. The selected "
            "difficulty can be tracked and discussed with a doctor or dietitian if intake is very limited.",
            risk="guided",
            steps=[
                "Keep meals predictable.",
                "Offer a tiny amount of one new food.",
                "Change only one feature at a time.",
                "Record accepted foods and concerns.",
            ],
            suggestions=[
                "How can I introduce new foods?",
                "Does diet cure autism?",
            ],
        )

    #finish the school support guide
    if flow_name == "school":
        return build_response(
            "School Support Guide",
            "Arrange a short meeting with the school and focus on the main concern and known trigger. "
            "Agree on a few practical supports and a date to review them.",
            risk="guided",
            steps=[
                "Share strengths and communication needs.",
                "Describe the trigger clearly.",
                "Choose one or two adjustments.",
                "Use a simple home-school update method.",
            ],
            suggestions=[
                "How can I talk to the teacher?",
                "What classroom accommodations may help?",
            ],
        )

    #finish the Malaysia resources guide
    return build_response(
        "Malaysia Resource Guide",
        "Start with the nearest appropriate health, school or JKM service and ask directly about "
        "referral, documents, costs and waiting time. Keep a written list of the answers.",
        risk="guided",
        steps=[
            "Prepare notes and existing reports.",
            "Contact the service before travelling.",
            "Ask about public referral and caregiver-training options.",
            "Check provider qualifications before paying.",
        ],
        suggestions=[
            "Where can I get autism support in Malaysia?",
            "What is JKM OKU registration?",
        ],
    )


#continue an active guided flow using the option selected by the user
def continue_flow(user_input):
    #get the current flow state from the session
    flow_state = session.get("flow")

    #return none when there is no active flow
    if flow_state is None:
        return None

    #allow the user to cancel the guide
    if clean_text(user_input) in ["cancel", "cancel guide", "stop", "exit"]:
        session.pop("flow", None)
        return build_response(
            "Guided Support",
            "The guide has been cancelled.",
            suggestions=DEFAULT_SUGGESTIONS,
        )

    #get the current flow and question
    flow = GUIDED_FLOWS[flow_state["name"]]
    current_question = flow["questions"][flow_state["step"]]

    #look for an option that matches the user's selected button
    selected_option = None
    for option in current_question["options"]:
        if clean_text(option) == clean_text(user_input):
            selected_option = option
            break

    #ask the user to select a listed option when the answer is not valid
    if selected_option is None:
        return build_response(
            flow["title"],
            "Please choose one of the listed options, or select Cancel guide.",
            risk="guided",
            suggestions=current_question["options"] + ["Cancel guide"],
            source="Guided rule-based support",
        )

    #save the selected answer using the question key
    flow_state["answers"][current_question["key"]] = selected_option

    #move to the next question
    flow_state["step"] += 1

    #save the changed flow state back into the session
    session["flow"] = flow_state

    #show the next question when the guide is not complete
    if flow_state["step"] < len(flow["questions"]):
        return get_flow_question(flow_state["name"])

    #finish the guide after the last answer
    return finish_flow(flow_state["name"], flow_state["answers"])


#check whether the user wants to start one of the guided flows
def check_flow_start(user_input):
    #clean the message before checking the trigger phrases
    text = clean_text(user_input)

    #check the start phrases of every guided flow
    for flow_name, flow in GUIDED_FLOWS.items():
        if contains_any_phrase(text, flow["start_phrases"]):
            return start_flow(flow_name)

    #return none when the user did not request a guide
    return None
