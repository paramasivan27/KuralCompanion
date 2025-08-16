import json
import os

# Load the aggregated thirukkural data with summaries
def load_aggregated_kurals():
    """Load the aggregated thirukkural data with chapter summaries"""
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'aggregated_thirukkural_with_summary.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error loading aggregated kurals: {e}")
        return {"chapters": []}

# Get the aggregated data
AGGREGATED_KURALS_DATA = load_aggregated_kurals()

def get_aggregated_chapters():
    """Get all chapters with their summaries"""
    return AGGREGATED_KURALS_DATA.get("chapters", [])

def get_chapter_by_name(chapter_name):
    """Get a specific chapter by name"""
    chapters = get_aggregated_chapters()
    for chapter in chapters:
        if chapter["Chapter"].lower() == chapter_name.lower():
            return chapter
    return None

def get_chapter_summary(chapter_name):
    """Get the summary for a specific chapter"""
    chapter = get_chapter_by_name(chapter_name)
    if chapter and "Summary" in chapter:
        return chapter["Summary"]
    return []

def get_kurals_by_chapter(chapter_name):
    """Get all kurals for a specific chapter"""
    chapter = get_chapter_by_name(chapter_name)
    if chapter and "Kurals" in chapter:
        return chapter["Kurals"]
    return []

def search_chapters_by_keyword(keyword):
    """Search chapters by keyword in chapter name or summary"""
    if not keyword:
        return []
    
    keyword_lower = keyword.lower()
    matching_chapters = []
    
    for chapter in get_aggregated_chapters():
        # Search in chapter name
        if keyword_lower in chapter["Chapter"].lower():
            matching_chapters.append(chapter)
            continue
        
        # Search in summary
        if "Summary" in chapter:
            for summary_point in chapter["Summary"]:
                if keyword_lower in summary_point.lower():
                    matching_chapters.append(chapter)
                    break
        
        # Search in kural content
        if "Kurals" in chapter:
            for kural in chapter["Kurals"]:
                if (keyword_lower in kural.get("Translation", "").lower() or
                    keyword_lower in kural.get("Explanation", "").lower() or
                    keyword_lower in kural.get("Couplet", "").lower()):
                    matching_chapters.append(chapter)
                    break
    
    return matching_chapters

def get_all_chapter_names():
    """Get all chapter names"""
    chapters = get_aggregated_chapters()
    return [chapter["Chapter"] for chapter in chapters]

def get_chapter_with_kurals_and_summary(chapter_name):
    """Get complete chapter data including kurals and summary"""
    return get_chapter_by_name(chapter_name)

# Enhanced RAG search function for aggregated data
def find_relevant_chapters_rag(user_input, emotions=None, themes=None):
    """Find relevant chapters using RAG approach with the aggregated data"""
    if not user_input:
        return []
    
    # Normalize inputs
    search_terms = [term.lower().strip() for term in user_input.lower().split() if len(term.strip()) > 2]
    detected_emotions = [e.lower() for e in (emotions or []) if e and e.lower() != "neutral"]
    detected_themes = [t.lower() for t in (themes or [])]
    
    scored_chapters = []  # (score, chapter, match_details)
    
    for chapter in get_aggregated_chapters():
        score = 0
        match_details = []
        
        # 1. Theme-based scoring
        chapter_name_lower = chapter["Chapter"].lower()
        for theme in detected_themes:
            if theme == chapter_name_lower:
                score += 20  # Exact theme match
                match_details.append(f"Exact theme match: {chapter['Chapter']}")
            elif theme in chapter_name_lower or chapter_name_lower in theme:
                score += 15  # Partial theme match
                match_details.append(f"Partial theme match: {chapter['Chapter']}")
        
        # 2. Summary-based scoring (unique to aggregated data)
        if "Summary" in chapter:
            summary_text = " ".join(chapter["Summary"]).lower()
            summary_matches = []
            summary_score = 0
            for term in search_terms:
                if term in summary_text:
                    term_weight = min(len(term), 6)  # Higher weight for summary matches
                    summary_score += term_weight
                    summary_matches.append(term)
            if summary_matches:
                score += summary_score
                match_details.append(f"Summary matches: {', '.join(summary_matches)}")
        
        # 3. Kural content scoring
        if "Kurals" in chapter:
            for kural in chapter["Kurals"]:
                # Search in Translation
                translation_text = kural.get("Translation", "").lower()
                for term in search_terms:
                    if term in translation_text:
                        score += 3
                        match_details.append(f"Translation match: {term}")
                
                # Search in Explanation
                explanation_text = kural.get("Explanation", "").lower()
                for term in search_terms:
                    if term in explanation_text:
                        score += 4
                        match_details.append(f"Explanation match: {term}")
                
                # Search in Couplet
                couplet_text = kural.get("Couplet", "").lower()
                for term in search_terms:
                    if term in couplet_text:
                        score += 2
                        match_details.append(f"Couplet match: {term}")
                
                # Emotion-based scoring
                if detected_emotions:
                    kural_emotions = str(kural.get("emotions", "")).lower()
                    for emotion in detected_emotions:
                        if emotion in kural_emotions:
                            score += 8
                            match_details.append(f"Emotion match: {emotion}")
        
        # 4. Contextual relevance scoring
        if score > 0:
            # Boost for comprehensive matches
            if len(match_details) >= 4:
                score += 8
            elif len(match_details) >= 3:
                score += 5
            
            # Boost for exact theme match with content matches
            if any("Exact theme match" in detail for detail in match_details):
                if any("Summary matches" in detail or "Translation match" in detail for detail in match_details):
                    score += 8
        
        # Only include chapters with meaningful scores
        if score >= 8:
            scored_chapters.append((score, chapter, match_details))
    
    # Sort by score (descending) and return top results
    scored_chapters.sort(key=lambda x: x[0], reverse=True)
    return [(chapter, details) for _, chapter, details in scored_chapters[:5]]
