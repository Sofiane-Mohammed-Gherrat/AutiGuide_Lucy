# --------------------------------------------------
# Topic categories used to organise the knowledge base
# --------------------------------------------------

from autiguide.text_processing import process_text


#store simple keywords used to guess the category of a question
CATEGORY_KEYWORDS = {
    "Autism Information": [
        "autism", "sign", "diagnosis", "cause", "vaccine", "spectrum",
        "lifelong", "early",
    ],
    "Behavioural Management": [
        "meltdown", "sensory", "aggression", "hitting", "biting",
        "stimming", "routine", "sleep", "wandering", "frustration",
    ],
    "Therapy and Intervention": [
        "therapy", "aba", "speech", "aac", "occupational",
        "intervention", "professional", "goal",
    ],
    "Dietary Guidance": [
        "eating", "selective", "texture", "nutrition", "diet",
        "supplement", "allergy", "vomiting",
    ],
    "School and Social Support": [
        "school", "friendship", "bullying", "homework", "learning",
    ],
    "Available Resources": [
        "malaysia", "jkm", "oku", "clinic", "hospital", "resource",
        "support", "assessment", "emergency",
    ],
}


#store the default buttons shown when no special suggestions are available
DEFAULT_SUGGESTIONS = [
    "What is ASD?",
    "What should I do during a meltdown?",
    "What is ABA therapy?",
    "My child is a picky eater",
    "How can I support my child at school?",
    "Where can I get autism support in Malaysia?",
]


#pre-process the category keyword lists once instead of on every message
_CATEGORY_WORD_SETS = {
    category: set(process_text(" ".join(keywords)))
    for category, keywords in CATEGORY_KEYWORDS.items()
}


#guess the broad category of the user's question
def detect_category(user_words):
    #convert the user's word list into a set for simple comparison
    user_word_set = set(user_words)

    #start without a detected category
    best_category = None
    best_score = 0

    #compare the user words with every category keyword list
    for category, category_words in _CATEGORY_WORD_SETS.items():
        #count the words shared by the user and this category
        score = len(user_word_set.intersection(category_words))

        #save the category when it has the highest score
        if score > best_score:
            best_score = score
            best_category = category

    #return none when no category keyword was found
    return best_category
