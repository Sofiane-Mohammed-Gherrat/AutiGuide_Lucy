from typing import List, Literal
from pydantic import BaseModel, Field


class QuestionSegment(BaseModel):
    
    original_snippet: str = Field(
        description="The exact text snippet or clause from the user's query that represents this specific issue."
    )
    category: Literal[
        
        'behaviour'
        
        ] = Field(
        description="The single most accurate category that applies *strictly* to this specific text snippet."
    )

    # 🌟 CRITICAL MOVE: Intent lives here now!
    intent: Literal[
        
        'definition', 
        'advice', 
        'prevention'
        
        ] = Field(
        description="The intent strictly for this specific text snippet (e.g., 'definition' for 'what is X', 'advice' for 'what to do')."
    )

    reformulated_question: str = Field(
        description="The snippet rewritten into a standalone, clear, and actionable question."
    )



class CaregiverResponse(BaseModel):
    query: str = Field(
        description="A grammatically correct, properly spelled version of the user's complete original text."
    )

    categorized_questions: List[QuestionSegment] = Field(
        description="Break down the original query into distinct, non-overlapping segments. Every distinct concern must have its own segment."
    ) 
    
    intent: Literal[
        
        'definition', 
        'advice', 
        'prevention'
        
        ]


'''class CaregiverResponse(BaseModel):
    query: str = Field(
        description="A grammatically correct, properly spelled version of the user's complete original text."
    )

    global_categories: List[Literal[
        
        'behaviour', 
        'communication', 
        'diagnosis', 
        'education', 
        'sensory', 
        'therapy'
        
        ]] = Field(
        description="A complete list of all unique categories identified across all segments."
    )
    

    categorized_questions: List[QuestionSegment] = Field(
        description="Break down the original query into distinct, non-overlapping segments. Every distinct concern must have its own segment."
    ) 
    
    intent: Literal[
        
        'definition', 
        'advice', 
        'prevention', 
        'general'
        
        ]

'''
