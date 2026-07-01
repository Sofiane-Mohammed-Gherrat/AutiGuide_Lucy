# --------------------------------------------------
# Safety expert system rules
# --------------------------------------------------
#
# These checks always run before normal knowledge base retrieval so
# that emergencies, medication questions, diagnosis requests, unsafe
# treatments and serious health symptoms never get a generic answer.

from autiguide.responses import build_response
from autiguide.text_processing import clean_text, contains_any_phrase


#store phrases that can show immediate danger
EMERGENCY_PHRASES = [
    "not breathing",
    "cannot breathe",
    "choking",
    "unconscious",
    "severe bleeding",
    "serious injury",
    "seizure",
    "trying to kill",
    "suicide",
    "child is missing",
    "cannot find my child",
    "cannot find the child",
    "ran away and is missing",
    "ran away and still missing",
]

#store phrases asking the chatbot to choose medication or dosage
MEDICATION_PHRASES = [
    "dosage",
    "prescription",
    "which medication",
    "what medication",
    "how much medication",
]

#store phrases asking the chatbot to diagnose a child
DIAGNOSIS_PHRASES = [
    "diagnose my child",
    "is my child autistic",
    "confirm autism",
    "does my child have autism",
]

#store unsafe treatment phrases that should never receive normal advice
UNSAFE_TREATMENT_PHRASES = [
    "bleach",
    "miracle mineral",
    "chelation",
    "detox cure",
    "cure autism with",
]

#store serious health symptoms that need professional assessment
HEALTH_WARNING_PHRASES = [
    "dehydrated",
    "dehydration",
    "fainting",
    "blood in stool",
    "persistent vomiting",
    "weight loss",
]


#check urgent, diagnosis, medication and unsafe treatment messages first
def check_safety_rules(user_input):
    #clean the user message before checking phrases
    text = clean_text(user_input)

    #return the emergency response before running normal retrieval
    if contains_any_phrase(text, EMERGENCY_PHRASES):
        return build_response(
            "Safety Alert",
            "This may be an emergency. Make the area as safe as you can without putting "
            "yourself in danger and call Malaysia Emergency Response Services on 999 now. "
            "AutiGuide cannot manage emergencies.",
            risk="emergency",
            steps=[
                "Call 999 and follow the operator's instructions.",
                "Stay with the child when it is safe to do so.",
                "Do not delay emergency care to continue chatting.",
            ],
            source="Malaysia Emergency Response Services 999",
        )

    #stop the chatbot from giving medication instructions
    if contains_any_phrase(text, MEDICATION_PHRASES):
        return build_response(
            "Medical Boundary",
            "AutiGuide cannot recommend medication, choose a drug or give dosage instructions. "
            "Please contact a doctor, pharmacist or other qualified healthcare professional.",
            risk="medical",
            suggestions=[
                "What can AutiGuide help with?",
                "How do I choose a therapist?",
            ],
        )

    #explain that diagnosis must be completed by a professional
    if contains_any_phrase(text, DIAGNOSIS_PHRASES):
        return build_response(
            "Assessment Guidance",
            "AutiGuide cannot diagnose autism. Record the behaviours and developmental concerns "
            "you have noticed and arrange an assessment with a qualified professional.",
            risk="medical",
            steps=[
                "Write down examples and when they occur.",
                "Ask school or other caregivers what they observe.",
                "Contact a doctor, paediatrician or child development service.",
            ],
            suggestions=[
                "What are common signs of autism?",
                "Where can I get an assessment in Malaysia?",
            ],
        )

    #warn the user about harmful or unverified treatments
    if contains_any_phrase(text, UNSAFE_TREATMENT_PHRASES):
        return build_response(
            "Unsafe Treatment Warning",
            "Do not use bleach, chelation or unverified detox products as autism treatments. "
            "They can be harmful. Speak with a qualified healthcare professional before starting "
            "a treatment or supplement.",
            risk="high",
            suggestions=[
                "How do I choose a trustworthy therapy?",
                "Does diet cure autism?",
            ],
        )

    #return a health warning when a serious symptom is found
    if contains_any_phrase(text, HEALTH_WARNING_PHRASES):
        return build_response(
            "Health Warning",
            "These symptoms need professional medical assessment. Contact a doctor promptly. "
            "Use 999 when there is breathing difficulty, loss of consciousness or immediate danger.",
            risk="high",
            suggestions=[
                "When is food refusal serious?",
                "When should I call emergency services?",
            ],
        )

    #return none when no safety rule is triggered
    return None
