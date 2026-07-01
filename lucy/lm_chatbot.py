import json
from .matcher import find_best_matches_for_segments
from .llm import llm_response

from sklearn.feature_extraction.text import TfidfVectorizer
from .preprocessing import preprocess

from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_FILE = BASE_DIR / "data" / "Knowledge_team.json"


# 1. Load Knowledge Base

with KNOWLEDGE_FILE.open("r", encoding="utf-8") as f:
    KNOWLEDGE = json.load(f)


# 2. Process Knowledge Base Documents

# Ensure it looks exactly like this:
documents = []
for entry in KNOWLEDGE:
    # Variables must be created locally inside the block
    text = (
        f"category {entry.get('category', '')} "
        f"subcategory {entry.get('subcategory', '')} "
        f"intent {entry.get('intent', '')} "
        f"title {entry.get('title', '')} "
        f"search questions {' '.join(entry["search_text"])} "
        #f"answer {entry.get('answer', '')}"
    )
    documents.append(preprocess(text))

# 3. Fit the Vectorizer
vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    lowercase=True
)
knowledge_vectors = vectorizer.fit_transform(documents)

THRESHOLD = 0.20

FALLBACK = (
    "I'm sorry, I don't have information about that."
    " Please consult a healthcare professional."
)


def join_answers(answered_segments: list[dict[str, str]]) -> str:
    sections = ["# Analysis of your query\n"]

    for i, item in enumerate(answered_segments, start=1):
        sections.append(
            f"""
### Concern {i} · {item['category'].title()}

> **Your concern:**  
> {item['sub_question']}

**Recommendation**

{item['answer']}

---
"""
        )

    return "\n".join(sections)

def get_response(question: str) -> str:
    # This list will now hold small summary dicts containing the question-answer pairs
    valid_answers_metadata = []

    response = llm_response(question)
    best_match = find_best_matches_for_segments(response, vectorizer, knowledge_vectors, KNOWLEDGE)

    for ele in best_match:
        score: float = ele['match_score']
        
        # Guard: Skip segments that are completely irrelevant mathematically
        if score < THRESHOLD:
            continue
            
        knowledge_data = ele.get('matched_knowledge', {})

        if isinstance(knowledge_data, dict):
            result_text: str = knowledge_data.get('answer', "No details available for this topic.")
        else:
            result_text: str = str(knowledge_data)
        
        # Package the context cleanly together
        valid_answers_metadata.append({
            "sub_question": ele.get('reformulated_question', 'General Concern'),
            "category": ele.get('category', 'general'),
            "answer": result_text
        })
    
    if len(valid_answers_metadata) > 0:
        formated_answer: str = join_answers(valid_answers_metadata)
    else:
        formated_answer: str = FALLBACK
    
    return formated_answer

if __name__=='__main__':
    question = 'what is a meltdown? and what to do during a meltdown?'
    #question = 'hi'
    print("\n--- Running End-to-End Chatbot Response ---")
    print(get_response(question))

    '''print('\n\n\nTesting\n\n')
    response = llm_response(question)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(response)
    best_match = find_best_matches_for_segments(response, vectorizer, knowledge_vectors, KNOWLEDGE)
    pp.pprint(best_match)
'''
