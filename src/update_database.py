"""
Script to update the Kural database files using thirukkural.json
Processes all 1330 kurals and organizes them into the three database files
"""

import json
from theme_classifier import process_kural_data, organize_by_theme

def load_thirukkural_json():
    """Load the thirukkural.json file"""
    with open('thirukkural.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['kural']

def split_kurals_by_sections(processed_kurals):
    """
    Split kurals into three sections for the three database files
    - kural_database.py: First 400 kurals (core database)
    - comprehensive_kurals.py: Next 400 kurals (comprehensive)
    - extended_kurals.py: Remaining 530 kurals (extended)
    """
    core_kurals = processed_kurals[:400]
    comprehensive_kurals = processed_kurals[400:800]
    extended_kurals = processed_kurals[800:]
    
    return core_kurals, comprehensive_kurals, extended_kurals

def create_database_file(kurals, filename, description):
    """Create a database file with the given kurals"""
    
    # Organize by theme
    theme_organized = organize_by_theme(kurals)
    
    # Create the file content
    content = f'''"""
{description}
Organized by themes and emotions for intelligent matching
"""

# {description}
KURAL_DATABASE = {{
'''
    
    # Add each theme
    for i, (theme, theme_kurals) in enumerate(theme_organized.items()):
        content += f'    "{theme}": [\n'
        
        for j, kural in enumerate(theme_kurals):
            # Use json.dumps to properly escape all text fields
            transliteration = json.dumps(kural["transliteration"], ensure_ascii=False)[1:-1]
            english = json.dumps(kural["english"], ensure_ascii=False)[1:-1]
            meaning = json.dumps(kural["meaning"], ensure_ascii=False)[1:-1]
            line1 = json.dumps(kural["line1"], ensure_ascii=False)[1:-1]
            line2 = json.dumps(kural["line2"], ensure_ascii=False)[1:-1]
            mv = json.dumps(kural["mv"], ensure_ascii=False)[1:-1]
            sp = json.dumps(kural["sp"], ensure_ascii=False)[1:-1]
            mk = json.dumps(kural["mk"], ensure_ascii=False)[1:-1]
            couplet = json.dumps(kural["couplet"], ensure_ascii=False)[1:-1]
            emotion_detail = json.dumps(kural.get("emotion_detail", ""), ensure_ascii=False)[1:-1]
            
            # Remove trailing comma for last item in theme
            comma = ',' if j < len(theme_kurals) - 1 else ''
            
            content += f'''        {{
            "number": {kural["number"]},
            "transliteration": "{transliteration}",
            "english": "{english}",
            "meaning": "{meaning}",
            "theme": "{kural["theme"]}",
            "emotions": {kural["emotions"]},
            "emotion_detail": "{emotion_detail}",
            "line1": "{line1}",
            "line2": "{line2}",
            "mv": "{mv}",
            "sp": "{sp}",
            "mk": "{mk}",
            "couplet": "{couplet}"
        }}{comma}\n'''
        
        # Remove trailing comma for last theme
        comma = ',' if i < len(theme_organized) - 1 else ''
        content += f'    ]{comma}\n'
    
    content += '}\n'
    
    # Write to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Created {filename} with {len(kurals)} kurals")

def update_emotion_keywords():
    """Update emotion keywords with new themes"""
    content = '''# Enhanced emotion keywords mapping
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
'''
    
    return content

def main():
    """Main function to update the database files"""
    print("Loading thirukkural.json...")
    kural_data = load_thirukkural_json()
    print(f"Loaded {len(kural_data)} kurals")
    
    print("Processing kural data...")
    processed_kurals = process_kural_data(kural_data)
    print(f"Processed {len(processed_kurals)} kurals")
    
    print("Splitting kurals into sections...")
    core_kurals, comprehensive_kurals, extended_kurals = split_kurals_by_sections(processed_kurals)
    
    print(f"Core kurals: {len(core_kurals)}")
    print(f"Comprehensive kurals: {len(comprehensive_kurals)}")
    print(f"Extended kurals: {len(extended_kurals)}")
    
    # Create the database files
    create_database_file(core_kurals, 'kural_database.py', 'Thirukkural Database - Core collection of 400 kurals')
    create_database_file(comprehensive_kurals, 'comprehensive_kurals.py', 'Comprehensive Thirukkural Database - Extended collection of 400 kurals')
    create_database_file(extended_kurals, 'extended_kurals.py', 'Extended Thirukkural Database - Complete collection of remaining kurals')
    
    # Update emotion keywords
    emotion_keywords_content = update_emotion_keywords()
    
    # Add emotion keywords to kural_database.py
    with open('kural_database.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the end of KURAL_DATABASE and add emotion keywords
    if '# Enhanced emotion keywords mapping' not in content:
        content += '\n\n' + emotion_keywords_content
    
    with open('kural_database.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Database files updated successfully!")
    print(f"Total kurals processed: {len(processed_kurals)}")
    print("Files created:")
    print("- kural_database.py (core kurals)")
    print("- comprehensive_kurals.py (comprehensive kurals)")
    print("- extended_kurals.py (extended kurals)")

if __name__ == "__main__":
    main() 