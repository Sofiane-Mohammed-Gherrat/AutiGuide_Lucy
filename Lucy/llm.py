from pydantic_logic import CaregiverResponse
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


def llm_response(query_text) -> str | List[Dict[str, str]]:

    response: CaregiverResponse = client.beta.chat.completions.parse(
        model="model-identifier", # LM studio will use whatever model is loaded
        messages=[
            {
            "role": "system", 
            "content": "You are classifying a caregiver question about autism."
            },
            {
            "role": "user", 
            "content": query_text
            }
        ],
        extra_body={
            "thinking": {
                "type": "enabled"  # Use "enabled" to turn it back on
            }
        },
        response_format=CaregiverResponse, # Pass the class here!
        temperature=0.2 # Lower temperature is recommended for data extraction
    )

    formated_answer = format_response(response.choices[0].message.parsed)

    return formated_answer
