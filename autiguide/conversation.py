# --------------------------------------------------
# General conversation
# --------------------------------------------------
#
# Handles the small-talk parts of the chatbot: greetings, thanks,
# help, "what are you" style questions, and "tell me more" follow-ups
# that repeat the last verified knowledge base answer.

from flask import session

from autiguide.categories import DEFAULT_SUGGESTIONS
from autiguide.responses import build_response
from autiguide.retrieval import ITEMS_BY_ID
from autiguide.text_processing import clean_text


#answer greetings, help questions and simple follow-up messages
def general_conversation(user_input):
    #clean the user message
    text = clean_text(user_input)

    #answer simple greetings
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
    if text in greetings:
        return build_response(
            "General Conversation",
            "Hello. I provide verified educational information for caregivers of autistic children. "
            "You can ask about behaviour, therapy, eating, school, autism information or Malaysian resources.",
            suggestions=DEFAULT_SUGGESTIONS,
        )

    #answer thank-you messages
    thanks = ["thanks", "thank you", "thank you very much"]
    if text in thanks:
        return build_response(
            "General Conversation",
            "You are welcome.",
            suggestions=DEFAULT_SUGGESTIONS,
        )

    #explain the topics supported by the chatbot
    help_messages = ["help", "what can you do", "what can i ask", "show examples"]
    if text in help_messages:
        return build_response(
            "Help",
            "Ask in your own words about autism information, behaviour, therapy, dietary guidance, "
            "school and social support or resources in Malaysia. I will not invent an answer when "
            "the knowledge base does not contain a reliable match.",
            suggestions=DEFAULT_SUGGESTIONS,
        )

    #explain what AutiGuide is
    identity_messages = ["who are you", "what is autiguide", "tell me about autiguide"]
    if text in identity_messages:
        return build_response(
            "About AutiGuide",
            "AutiGuide is a retrieval-based chatbot with rule-based safety checks. Normal answers "
            "come only from its prepared knowledge base. It is not a diagnostic or treatment system.",
            suggestions=DEFAULT_SUGGESTIONS,
        )

    #repeat the previous verified topic when the user asks for more
    follow_up_messages = ["more", "tell me more", "explain more", "continue"]
    if text in follow_up_messages:
        #get the id of the previous knowledge base item
        last_item_id = session.get("last_item_id")

        #find the complete item using its id
        previous_item = ITEMS_BY_ID.get(last_item_id)

        #return the previous answer when it exists
        if previous_item is not None:
            return build_response(
                previous_item["category"],
                previous_item["answer"],
                risk=previous_item["risk_level"],
                steps=previous_item["steps"],
                suggestions=previous_item["suggestions"],
                source=previous_item["source_type"],
                confidence="follow-up",
                item=previous_item,
            )

        #ask for a topic when there is no previous answer
        return build_response(
            "Follow-up",
            "Please name the topic you want to continue.",
            suggestions=DEFAULT_SUGGESTIONS,
        )

    #return none when the message is not general conversation
    return None
