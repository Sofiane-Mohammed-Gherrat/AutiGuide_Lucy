import numpy as np
from typing import List, Dict, Any
from sklearn.metrics.pairwise import cosine_similarity
from .preprocessing import preprocess

# ---- Configuring the number of matches to pull and compare 
TOP_K = 6


def find_best_matches_for_segments(
    flattened_segments: List[Dict[str, Any]],
    vectorizer,
    knowledge_vectors,  
    knowledge_base: List[Dict[str, Any]],
    score_threshold: float = 0.15
) -> List[Dict[str, Any]]:
    
    processed_results = []

    for segment in flattened_segments:
        # CRITICAL FIX 1: Variables MUST reset to defaults for EVERY single segment row
        best_filtered_match = None
        fallback_match = None

        best_final_score = -1.0      # Used for ranking
        best_cosine_score = -1.0     # Optional: keep original cosine score
        
        text_to_match = segment.get('reformulated_question', '')
        # 🌟 FIXED: Pull the intent assigned strictly to THIS segment
        llm_intent = str(segment.get('intent', '')).lower().strip() 
        llm_category = str(segment.get('category', '')).lower().strip()
        
        # 1. Vectorize the segment text
        processed = preprocess(text_to_match)
        query_vector = vectorizer.transform([processed])
        
        # 2. Get similarities for ALL knowledge base entries
        similarity_scores = cosine_similarity(query_vector, knowledge_vectors)[0]
        
        # 3. Get indices of the top 3 highest scores
        top_indices = np.argsort(similarity_scores)[-TOP_K:][::-1]
        
        # 4. Iterate through top 3 candidates to apply the Intent Filter
        for idx in top_indices:
            score = float(similarity_scores[idx])
            candidate_kb = knowledge_base[idx]
            
            if score < score_threshold:
                continue

            fallback_cosine_score = -1.0
                
            if fallback_match is None:
                fallback_match = candidate_kb
                fallback_cosine_score = score

            
            # Extract KB fields
            kb_category = str(candidate_kb.get('category', '')).lower().strip()
            kb_subcategory = str(candidate_kb.get('subcategory', '')).lower().strip()
            kb_intent = str(candidate_kb.get('intent', '')).lower().strip()
            kb_title = str(candidate_kb.get('title', '')).lower().strip()
            
            # Advanced Context matching
            kb_search_text = " ".join(candidate_kb.get('search_text', [])).lower() if isinstance(candidate_kb.get('search_text'), list) else str(candidate_kb.get('search_text', '')).lower()
            kb_all_context = f"{kb_category} {kb_subcategory} {kb_title} {kb_search_text}"

            category_match = (
                llm_category == kb_category or 
                llm_category in kb_subcategory or 
                llm_category in kb_all_context
            )

            intent_match = (
                llm_intent == kb_intent or 
                llm_intent in kb_title or
                llm_intent in kb_all_context
            )
            final_score = score

            if score >= 0.25:
                if category_match:
                    final_score += 0.10

                if intent_match:
                    final_score += 0.15

                if llm_intent and llm_intent in kb_title:
                    final_score += 0.05

            # Keep the highest-ranked candidate
            if final_score > best_final_score:
                best_final_score = final_score
                best_cosine_score = score
                best_filtered_match = candidate_kb


        # CRITICAL FIX 2: Rebuild a brand-new dict explicitly instead of shallow copying
        matched_segment = {
            'original_query': segment.get('original_query'),
            'global_intent': segment.get('global_intent'),
            'snippet': segment.get('snippet'),
            'category': segment.get('category'),
            'reformulated_question': segment.get('reformulated_question')
        }
        
        if best_filtered_match:
            matched_segment['matched_knowledge'] = best_filtered_match
            matched_segment['match_score'] = best_cosine_score
            matched_segment['ranking_score'] = best_final_score
            matched_segment['filter_status'] = "Verified by Intent Filter"
        elif fallback_match:
            matched_segment['matched_knowledge'] = fallback_match
            matched_segment["match_score"] = fallback_cosine_score
            matched_segment['ranking_score'] = best_final_score
            matched_segment['filter_status'] = "Fallback (Filter Unmatched)"
        else:
            matched_segment['matched_knowledge'] = None
            matched_segment['match_score'] = 0.0
            matched_segment['filter_status'] = "No relevant match found"

        processed_results.append(matched_segment)
        
    return processed_results
