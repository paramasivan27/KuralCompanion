"""
Thirukkural Database Loader
Loads kurals from JSON files and provides database functions
"""

import json
import os

_SRC_DIR = os.path.dirname(os.path.abspath(__file__))

def load_database(filename):
    """Load a database from JSON file"""
    path = os.path.join(_SRC_DIR, filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"metadata": {}, "kurals": {}}

# Load all databases
CORE_DB = load_database('kural_database.json')
COMPREHENSIVE_DB = load_database('comprehensive_kurals.json')
EXTENDED_DB = load_database('extended_kurals.json')

# Combine all databases
def get_comprehensive_database():
    """Get the comprehensive database combining all kurals"""
    combined = {}
    
    # Add kurals from all databases
    for db in [CORE_DB, COMPREHENSIVE_DB, EXTENDED_DB]:
        if "kurals" in db:
            for theme, kurals in db["kurals"].items():
                if theme not in combined:
                    combined[theme] = []
                combined[theme].extend(kurals)
    
    return combined

# Main database
KURAL_DATABASE = get_comprehensive_database()

# Enhanced emotion keywords mapping
EMOTION_KEYWORDS = {
    "sad": ["sad", "depressed", "lonely", "heartbroken", "grief", "sorrow", "pain", "hurt", "crying", "tears", "melancholy", "despair", "hopeless", "miserable"],
    "angry": ["angry", "furious", "rage", "hate", "resentment", "bitter", "hostile", "irritated", "annoyed", "mad", "livid", "outraged", "fuming"],
    "confused": ["confused", "uncertain", "doubt", "question", "why", "how", "what", "unsure", "puzzled", "perplexed", "bewildered", "lost", "uncertainty"],
    "grateful": ["thankful", "grateful", "blessed", "appreciate", "gratitude", "thank", "blessing", "fortunate", "lucky", "appreciative"],
    "love": ["love", "romance", "relationship", "marriage", "family", "care", "affection", "heart", "adore", "cherish", "treasure"],
    "wisdom": ["wisdom", "knowledge", "learn", "teach", "understand", "truth", "philosophy", "meaning", "insight", "enlightenment"],
    "fear": ["fear", "afraid", "scared", "anxiety", "worry", "nervous", "terrified", "panic", "dread", "apprehensive", "frightened"],
    "joy": ["happy", "joy", "excited", "celebrate", "success", "achievement", "victory", "triumph", "elated", "thrilled", "ecstatic"],
    "peaceful": ["peaceful", "calm", "serene", "tranquil", "forgiving", "compassionate", "merciful", "content", "relaxed", "at_ease"],
    "patient": ["patient", "tolerant", "enduring", "persevering", "waiting", "steady", "persistent", "resilient"],
    "courage": ["brave", "courageous", "bold", "fearless", "daring", "heroic", "valiant", "confident", "strong"],
    "humility": ["humble", "modest", "meek", "unassuming", "unpretentious", "down_to_earth", "simple"],
    "gratitude": ["thankful", "grateful", "appreciative", "blessed", "fortunate", "indebted"],
    "reverent": ["reverent", "devoted", "worshipful", "sacred", "holy", "spiritual"],
    "thoughtful": ["thoughtful", "contemplative", "reflective", "meditative", "introspective"],
    "principled": ["principled", "moral", "ethical", "righteous", "virtuous", "upright"],
    "confident": ["confident", "assured", "self-assured", "bold", "decisive"],
    "content": ["content", "satisfied", "fulfilled", "happy", "pleased"],
    "loyal": ["loyal", "faithful", "devoted", "dedicated", "committed"],
    "loving": ["loving", "caring", "nurturing", "affectionate", "tender"],
    "calm": ["calm", "serene", "peaceful", "tranquil", "composed"],
    "brave": ["brave", "courageous", "fearless", "bold", "valiant"],
    "modest": ["modest", "humble", "unassuming", "unpretentious", "simple"],
    "compassionate": ["compassionate", "merciful", "kind", "gentle", "benevolent"],
    "passionate": ["passionate", "ardent", "fervent", "enthusiastic", "zealous"],
    "eloquent": ["eloquent", "articulate", "expressive", "fluent", "well-spoken"],
    "active": ["active", "energetic", "dynamic", "vigorous", "lively"],
    "patient": ["patient", "enduring", "persevering", "steadfast", "resilient"],
    "anxious": ["anxious", "worried", "concerned", "nervous", "uneasy"],
    "furious": ["furious", "enraged", "irate", "livid", "incensed"],
    "desirous": ["desirous", "eager", "yearning", "longing", "craving"],
    "fair": ["fair", "just", "equitable", "impartial", "unbiased"]
}

# Enhanced theme keywords mapping
THEME_KEYWORDS = {
    "divine_love": ["god", "lord", "divine", "eternal", "supreme", "creator", "almighty", "deity", "worship", "prayer", "devotion", "sacred", "holy", "spiritual"],
    "wisdom": ["wisdom", "knowledge", "learn", "teach", "understand", "truth", "philosophy", "insight"],
    "ethics": ["right", "wrong", "moral", "ethical", "good", "bad", "virtue", "sin", "morality", "principles"],
    "leadership": ["leader", "king", "ruler", "govern", "manage", "authority", "power", "command", "direct"],
    "wealth": ["money", "wealth", "rich", "poor", "poverty", "fortune", "prosperity", "riches", "affluence"],
    "friendship": ["friend", "friendship", "companion", "ally", "buddy", "mate", "comrade", "partner"],
    "family": ["family", "parent", "child", "son", "daughter", "mother", "father", "home", "household"],
    "patience": ["patience", "patient", "wait", "endure", "persevere", "tolerance", "endurance"],
    "courage": ["brave", "courage", "bold", "fearless", "daring", "heroic", "valiant"],
    "humility": ["humble", "modest", "meek", "unassuming", "simple", "down_to_earth"],
    "gratitude": ["thankful", "grateful", "appreciative", "blessed", "fortunate"],
    "forgiveness": ["forgive", "forgiveness", "pardon", "excuse", "mercy", "compassion", "clemency"],
    "love": ["love", "romance", "marriage", "relationship", "heart", "affection", "passion", "intimacy"],
    "speech": ["speech", "word", "talk", "speak", "language", "communication", "eloquence", "oratory"],
    "action": ["action", "deed", "work", "labor", "effort", "activity", "performance", "conduct"],
    "time": ["time", "moment", "hour", "day", "night", "season", "period", "duration"],
    "fear": ["fear", "afraid", "scared", "terror", "dread", "fright", "panic", "anxiety"],
    "anger": ["angry", "rage", "fury", "wrath", "ire", "temper", "outrage", "indignation"],
    "greed": ["greed", "avarice", "covetousness", "desire", "lust", "craving", "yearning"],
    "justice": ["justice", "fair", "just", "equity", "righteousness", "law", "judgment", "court"]
}

def get_all_kurals():
    """Get all kurals from the database"""
    all_kurals = []
    for theme, kurals in KURAL_DATABASE.items():
        all_kurals.extend(kurals)
    return all_kurals

def get_kural_by_number(number):
    """Get a specific kural by its number"""
    all_kurals = get_all_kurals()
    for kural in all_kurals:
        if kural["number"] == number:
            return kural
    return None

def get_kurals_by_theme(theme):
    """Get all kurals for a specific theme"""
    return KURAL_DATABASE.get(theme, [])

def get_kurals_by_emotion(emotion):
    """Get all kurals that match a specific emotion"""
    matching_kurals = []
    for theme, kurals in KURAL_DATABASE.items():
        for kural in kurals:
            if emotion in kural.get("emotions", []):
                matching_kurals.append(kural)
    return matching_kurals

def search_kurals_by_keyword(keyword):
    """Search kurals by keyword in English meaning or Tamil text"""
    matching_kurals = []
    keyword_lower = keyword.lower()
    
    for theme, kurals in KURAL_DATABASE.items():
        for kural in kurals:
            # Combine line1 and line2 for Tamil text search
            tamil_text = f"{kural.get('line1', '')} {kural.get('line2', '')}".strip()
            if (keyword_lower in kural["english"].lower() or 
                keyword_lower in kural["meaning"].lower() or
                keyword_lower in tamil_text.lower()):
                matching_kurals.append(kural)
    
    return matching_kurals

def get_total_kural_count():
    """Get the total number of kurals in the comprehensive database"""
    total_count = 0
    for theme, kurals in KURAL_DATABASE.items():
        total_count += len(kurals)
    return total_count

def get_theme_counts():
    """Get the count of kurals for each theme"""
    theme_counts = {}
    for theme, kurals in KURAL_DATABASE.items():
        theme_counts[theme] = len(kurals)
    return theme_counts
