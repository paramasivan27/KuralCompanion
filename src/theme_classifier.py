"""
Theme Classifier for Thirukkural
Automatically categorizes kurals based on their translation and explanation
"""

import re

# Theme keywords for classification
THEME_KEYWORDS = {
    "divine_love": ["god", "lord", "divine", "eternal", "supreme", "creator", "almighty", "deity", "worship", "prayer", "devotion", "sacred", "holy", "spiritual"],
    "wisdom": ["wisdom", "knowledge", "learn", "learning", "study", "education", "intelligence", "understanding", "comprehension", "insight", "enlightenment"],
    "ethics": ["right", "wrong", "moral", "ethical", "virtue", "sin", "good", "bad", "morality", "principles", "duty", "obligation", "responsibility"],
    "leadership": ["leader", "king", "ruler", "govern", "manage", "authority", "power", "command", "direct", "rule", "administration"],
    "wealth": ["money", "wealth", "rich", "poor", "poverty", "fortune", "prosperity", "riches", "affluence", "treasure", "gold", "silver"],
    "friendship": ["friend", "friendship", "companion", "ally", "buddy", "mate", "comrade", "partner", "loyalty", "trust"],
    "family": ["family", "parent", "child", "son", "daughter", "mother", "father", "home", "household", "domestic"],
    "patience": ["patience", "patient", "wait", "endure", "persevere", "tolerance", "endurance", "steadfast", "persistent"],
    "courage": ["brave", "courage", "bold", "fearless", "daring", "heroic", "valiant", "confident", "strong", "boldness"],
    "humility": ["humble", "modest", "meek", "unassuming", "unpretentious", "down_to_earth", "simple", "modesty"],
    "gratitude": ["thankful", "grateful", "appreciative", "blessed", "fortunate", "indebted", "thank", "blessing"],
    "forgiveness": ["forgive", "forgiveness", "pardon", "excuse", "mercy", "compassion", "clemency", "absolve"],
    "love": ["love", "romance", "marriage", "relationship", "heart", "affection", "passion", "intimacy", "romantic"],
    "speech": ["speech", "word", "talk", "speak", "language", "communication", "eloquence", "oratory", "rhetoric"],
    "action": ["action", "deed", "work", "labor", "effort", "activity", "performance", "conduct", "behavior"],
    "time": ["time", "moment", "hour", "day", "night", "season", "period", "duration", "temporal"],
    "fear": ["fear", "afraid", "scared", "terror", "dread", "fright", "panic", "anxiety", "worry"],
    "anger": ["angry", "rage", "fury", "wrath", "ire", "temper", "outrage", "indignation"],
    "greed": ["greed", "avarice", "covetousness", "desire", "lust", "craving", "yearning", "hunger"],
    "justice": ["justice", "fair", "just", "equity", "righteousness", "law", "judgment", "court", "trial"]
}

def classify_theme(translation, explanation, mv, sp, mk):
    """
    Classify the theme of a kural based on its translation and explanations
    """
    # Combine all text for analysis
    text = f"{translation} {explanation} {mv} {sp} {mk}".lower()
    
    # Count theme matches
    theme_scores = {}
    
    for theme, keywords in THEME_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in text:
                score += 1
        if score > 0:
            theme_scores[theme] = score
    
    # Return the theme with highest score, or default to wisdom
    if theme_scores:
        return max(theme_scores, key=theme_scores.get)
    else:
        return "wisdom"

def get_emotions_for_theme(theme):
    """
    Get appropriate emotions for a given theme
    """
    emotion_mapping = {
        "divine_love": ["reverent", "devoted", "grateful"],
        "wisdom": ["thoughtful", "contemplative", "enlightened"],
        "ethics": ["principled", "moral", "righteous"],
        "leadership": ["confident", "authoritative", "responsible"],
        "wealth": ["content", "satisfied", "prosperous"],
        "friendship": ["loyal", "trusting", "caring"],
        "family": ["loving", "nurturing", "protective"],
        "patience": ["calm", "steady", "persistent"],
        "courage": ["brave", "fearless", "determined"],
        "humility": ["modest", "humble", "unassuming"],
        "gratitude": ["thankful", "appreciative", "blessed"],
        "forgiveness": ["compassionate", "merciful", "kind"],
        "love": ["passionate", "affectionate", "romantic"],
        "speech": ["eloquent", "articulate", "expressive"],
        "action": ["active", "energetic", "productive"],
        "time": ["patient", "mindful", "aware"],
        "fear": ["anxious", "worried", "nervous"],
        "anger": ["furious", "irritated", "angry"],
        "greed": ["desirous", "covetous", "greedy"],
        "justice": ["fair", "just", "righteous"]
    }
    
    return emotion_mapping.get(theme, ["wise", "thoughtful", "contemplative"])

def process_kural_data(kural_data):
    """
    Process kural data from JSON format to our database format
    """
    processed_kurals = []
    
    for kural in kural_data:
        # Extract data
        number = kural["Number"]
        line1 = kural["Line1"]
        line2 = kural["Line2"]
        translation = kural["Translation"]
        explanation = kural["explanation"]
        mv = kural.get("mv", "")
        sp = kural.get("sp", "")
        mk = kural.get("mk", "")
        couplet = kural.get("couplet", "")
        transliteration1 = kural.get("transliteration1", "")
        transliteration2 = kural.get("transliteration2", "")
        
        # Classify theme
        theme = classify_theme(translation, explanation, mv, sp, mk)
        
        # Get emotions
        emotions = get_emotions_for_theme(theme)
        
        # Create processed kural
        processed_kural = {
            "number": number,
            "tamil": f"{line1} {line2}",
            "transliteration": f"{transliteration1} {transliteration2}",
            "english": translation,
            "meaning": explanation,
            "theme": theme,
            "emotions": emotions,
            "line1": line1,
            "line2": line2,
            "mv": mv,
            "sp": sp,
            "mk": mk,
            "couplet": couplet
        }
        
        processed_kurals.append(processed_kural)
    
    return processed_kurals

def organize_by_theme(processed_kurals):
    """
    Organize processed kurals by theme
    """
    theme_organized = {}
    
    for kural in processed_kurals:
        theme = kural["theme"]
        if theme not in theme_organized:
            theme_organized[theme] = []
        theme_organized[theme].append(kural)
    
    return theme_organized 