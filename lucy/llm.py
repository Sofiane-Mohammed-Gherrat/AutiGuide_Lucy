from .pydantic_logic import CaregiverResponse
from typing import Dict, List
from openai import OpenAI



# --------------------------------------------------------------------
# Client:
# --------------------------------------------------------------------
client = OpenAI(
    base_url="http://localhost:1234/v1", 
    api_key="lm-studio"
    )

# Query Example 
query_text = "My chxbild gets highly aggressive and covers theiezjvr eazoodars wvhenever the vacuum turns on. What should I éeiuudo? and me3y child is having difficulties speaking"

def format_response(response) -> CaregiverResponse | List[Dict[str, str]]: 
    
    flattened_data = []
    
    for segment in response.categorized_questions:
        row = {
        "original_query": response.query,
        "intent": segment.intent,
        "snippet": segment.original_snippet,
        "category": segment.category,
        "reformulated_question": segment.reformulated_question
        }
        flattened_data.append(row)
    
    return flattened_data


def llm_response(query_text: str) -> List[Dict[str, str]]:
    try:
        response = client.beta.chat.completions.parse(
            model="model-identifier",
            messages=[
                {"role": "system", "content": "You are classifying a caregiver question about autism."},
                {"role": "user", "content": query_text},
            ],
            extra_body={"thinking": {"type": "enabled"}},
            response_format=CaregiverResponse,
            temperature=0.2,
        )
    except Exception as e:
        print(f"[llm_response] LM Studio call failed: {e}")
        return []

    parsed = response.choices[0].message.parsed
    if parsed is None or not parsed.categorized_questions:
        return []

    return format_response(parsed)
