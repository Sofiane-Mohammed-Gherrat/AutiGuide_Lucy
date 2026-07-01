# --------------------------------------------------
# Text cleaning, normalisation and simple word processing
# --------------------------------------------------
#
# This module has no dependencies on Flask or the knowledge base.
# It only turns raw user text into a clean list of useful words,
# so it can be tested and reused on its own.

import re


#store common words that do not strongly describe the user's topic
STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been",
    "to", "of", "for", "in", "on", "at", "with", "and", "or",
    "that", "this", "it", "my", "his", "her", "their", "our",
    "your", "i", "we", "you", "he", "she", "they", "do", "does",
    "did", "can", "could", "would", "should", "please", "tell",
    "explain", "about", "what", "how", "why",
}


#store words that should have the same meaning during matching
SYNONYMS = {
    #autism words
    "asd": "autism",
    "autistic": "autism",

    #child words
    "kid": "child",
    "kids": "child",
    "son": "child",
    "daughter": "child",
    "boy": "child",
    "girl": "child",

    #meltdown and sensory words
    "tantrum": "meltdown",
    "screaming": "meltdown",
    "crying": "meltdown",
    "overstimulated": "sensory",
    "overstimulation": "sensory",
    "noise": "sensory",
    "noisy": "sensory",
    "loud": "sensory",
    "sound": "sensory",
    "lights": "sensory",
    "vacuum": "sensory",
    "blender": "sensory",
    "appliance": "sensory",
    "appliances": "sensory",
    "ears": "sensory",

    #aggression words
    "hit": "hitting",
    "hits": "hitting",
    "bite": "biting",
    "bites": "biting",
    "kick": "kicking",
    "kicks": "kicking",
    "violent": "aggression",
    "aggressive": "aggression",
    "angry": "frustration",

    #communication words
    "nonverbal": "communication",
    "nonspeaking": "communication",
    "talk": "communication",
    "speaking": "communication",

    #food words
    "food": "eating",
    "foods": "eating",
    "meal": "eating",
    "meals": "eating",
    "picky": "selective",

    #school words
    "teacher": "school",
    "classroom": "school",
    "classmate": "school",
    "classmates": "school",
    "friends": "friendship",

    #professional and medicine words
    "doctor": "professional",
    "paediatrician": "professional",
    "pediatrician": "professional",
    "therapist": "professional",
    "medicine": "medication",
    "dose": "dosage",
}


#clean the text before matching it with the knowledge base
def clean_text(text):
    #convert all letters to lowercase
    text = text.lower()

    #replace punctuation and special characters with spaces
    text = re.sub(r"[^a-z0-9\s'-]", " ", text)

    #replace repeated spaces with one space
    text = re.sub(r"\s+", " ", text)

    #remove spaces from the beginning and end
    return text.strip()


#change one word into a simple standard form
def normalise_word(word):
    #return the synonym immediately when the word exists in the dictionary
    if word in SYNONYMS:
        return SYNONYMS[word]

    #remove only a few common endings to keep the stemmer simple
    if word.endswith("ing") and len(word) > 6:
        word = word[:-3]
    elif word.endswith("ed") and len(word) > 5:
        word = word[:-2]
    elif word.endswith("es") and len(word) > 5:
        word = word[:-2]
    elif word.endswith("s") and len(word) > 4:
        word = word[:-1]

    #check the synonym dictionary again after removing the ending
    return SYNONYMS.get(word, word)


#convert a sentence into useful words for matching
def process_text(text):
    #clean the complete sentence first
    cleaned_text = clean_text(text)

    #create an empty list for the useful words
    useful_words = []

    #check every word in the sentence
    for word in cleaned_text.split():
        #ignore stop words and one-letter words
        if word in STOP_WORDS or len(word) <= 1:
            continue

        #normalise the word and add it to the list
        useful_words.append(normalise_word(word))

    #return the processed words
    return useful_words


#check whether the cleaned text contains one of the listed phrases
def contains_any_phrase(text, phrases):
    #check every phrase one by one
    for phrase in phrases:
        if phrase in text:
            return True

    #return false when no phrase is found
    return False
