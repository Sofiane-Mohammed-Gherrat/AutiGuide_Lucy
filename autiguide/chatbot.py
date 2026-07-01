# --------------------------------------------------
# Main chatbot decision function
# --------------------------------------------------
#
# This is the single entry point the Flask route calls. It decides,
# in priority order, which part of the chatbot should handle the
# user's message: safety rules first, then an active guided flow,
# then starting a new guided flow, then general conversation, and
# finally the knowledge base itself.

from autiguide.conversation import general_conversation
from autiguide.guided_flows import check_flow_start, continue_flow
from autiguide.retrieval import retrieve_answer
from autiguide.safety import check_safety_rules


#decide which part of the chatbot should handle the user's message
def get_autiguide_response(user_input):
    #check safety rules before every other feature
    response = check_safety_rules(user_input)
    if response is not None:
        return response

    #continue an active guided flow before normal retrieval
    response = continue_flow(user_input)
    if response is not None:
        return response

    #start a guided flow when the user requests one
    response = check_flow_start(user_input)
    if response is not None:
        return response

    #answer greetings, help and follow-up messages
    response = general_conversation(user_input)
    if response is not None:
        return response

    #use the knowledge base for all remaining questions
    return retrieve_answer(user_input)
