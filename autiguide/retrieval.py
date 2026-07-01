# --------------------------------------------------
# Knowledge base retrieval
# --------------------------------------------------
#
# This module owns everything to do with finding the best matching
# knowledge base entry for a user's message, and falling back safely
# when there is no reliable match.

from knowledge_base import knowledge_base

from autiguide.categories import DEFAULT_SUGGESTIONS, detect_category
from autiguide.responses import build_response
from autiguide.text_processing import clean_text, process_text


#create a dictionary that finds an item directly by its id
ITEMS_BY_ID = {item["id"]: item for item in knowledge_base}


#prepare the question words and keyword words once when the application starts
def prepare_search_data():
    #create an empty list for prepared knowledge base records
    prepared_items = []

    #go through every item in the knowledge base
    for item in knowledge_base:
        #process the stored question
        question_words = set(process_text(item["question"]))

        #process the stored keyword list
        keyword_text = " ".join(item["keywords"])
        keyword_words = set(process_text(keyword_text))

        #store the original item with its processed words
        prepared_items.append({
            "item": item,
            "question_words": question_words,
            "keyword_words": keyword_words,
        })

    #return all prepared records
    return prepared_items


#prepare the records once instead of repeating this work for every message
SEARCH_DATA = prepare_search_data()


#calculate a simple matching score for one knowledge base item
def calculate_match_score(user_input, user_words, prepared_item, category):
    #get the original item and its prepared word sets
    item = prepared_item["item"]
    question_words = prepared_item["question_words"]
    keyword_words = prepared_item["keyword_words"]

    #convert the user's words into a set
    user_word_set = set(user_words)

    #count words shared with the stored question
    question_matches = len(user_word_set.intersection(question_words))

    #count words shared with the stored keywords
    keyword_matches = len(user_word_set.intersection(keyword_words))

    #give question words more importance than general keywords
    score = (question_matches * 4) + (keyword_matches * 2)

    #give a large bonus when the user's question exactly matches a stored question
    exact_match = clean_text(user_input) == clean_text(item["question"])
    if exact_match:
        score += 20

    #give a small bonus when the detected category is also correct
    if category == item["category"]:
        score += 1

    #count the total number of useful words shared with this item
    all_item_words = question_words.union(keyword_words)
    matched_words = len(user_word_set.intersection(all_item_words))

    #return the score and matching information
    return score, matched_words, exact_match


#find the best knowledge base item for the user's question
def find_best_match(user_input):
    #process the user's message
    user_words = process_text(user_input)

    #stop when the message has no useful words
    if not user_words:
        return None, 0, 0, None, False

    #detect the broad category of the question
    category = detect_category(user_words)

    #store the best result found so far
    best_item = None
    best_score = 0
    best_matched_words = 0
    best_exact_match = False

    #compare the user question with every prepared knowledge base item
    for prepared_item in SEARCH_DATA:
        score, matched_words, exact_match = calculate_match_score(
            user_input,
            user_words,
            prepared_item,
            category,
        )

        #replace the best result when this item has a higher score
        if score > best_score:
            best_item = prepared_item["item"]
            best_score = score
            best_matched_words = matched_words
            best_exact_match = exact_match

    #return the best result and its matching information
    return best_item, best_score, best_matched_words, category, best_exact_match


#return suggestions related to a detected category
def get_category_suggestions(category):
    #use the default suggestions when no category was detected
    if category is None:
        return DEFAULT_SUGGESTIONS

    #create an empty list for category questions
    suggestions = []

    #collect the first three questions belonging to the category
    for item in knowledge_base:
        if item["category"] == category:
            suggestions.append(item["question"])

        if len(suggestions) == 3:
            break

    #return the category suggestions
    return suggestions


#return a safe fallback when the chatbot has no reliable match
def fallback_response(category=None):
    #get suitable buttons for the detected category
    suggestions = get_category_suggestions(category)

    #tell the user that the chatbot will not guess
    return build_response(
        category or "No Reliable Match",
        "I could not find a sufficiently reliable answer in my prepared knowledge base. "
        "Please rephrase the question or choose a related suggestion. I will not guess.",
        suggestions=suggestions,
        source="Retrieval safety gate",
        confidence="low",
    )


#retrieve the most suitable prepared answer from the knowledge base
def retrieve_answer(user_input):
    #find the highest-scoring knowledge base item
    item, score, matched_words, category, exact_match = find_best_match(user_input)

    #return the fallback when no item was found
    if item is None:
        return fallback_response(category)

    #accept an exact question or a result with enough simple word matches
    reliable_match = exact_match or (score >= 5 and matched_words >= 1)

    #do not return the item when the match is too weak
    if not reliable_match:
        return fallback_response(category)

    #show high confidence for a strong score and medium confidence otherwise
    if exact_match or score >= 10:
        match_quality = "high"
    else:
        match_quality = "medium"

    #return the verified item without generating a new answer
    return build_response(
        item["category"],
        item["answer"],
        risk=item["risk_level"],
        steps=item["steps"],
        suggestions=item["suggestions"],
        source=item["source_type"],
        confidence=match_quality,
        item=item,
    )
