import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from textblob import TextBlob
import re
from collections import defaultdict
import json
from streamlit_option_menu import option_menu

# Page configuration
st.set_page_config(
    page_title="KuralCompanion - Ancient Wisdom for Modern Life",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .kural-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .emotion-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        margin: 0.25rem;
    }
    .emotion-sad { background-color: #ff6b6b; }
    .emotion-happy { background-color: #4ecdc4; }
    .emotion-angry { background-color: #ff8a80; }
    .emotion-confused { background-color: #a8e6cf; }
    .emotion-grateful { background-color: #ffd93d; }
    .emotion-love { background-color: #ff69b4; }
    .emotion-wisdom { background-color: #6c5ce7; }
    .emotion-peaceful { background-color: #74b9ff; }
    .emotion-patient { background-color: #a29bfe; }
</style>
""", unsafe_allow_html=True)

# Thirukkural Database
KURAL_DATABASE = {
    "love": [
        {
            "number": 1,
            "tamil": "அகர முதல எழுத்தெல்லாம் ஆதி பகவன் முதற்றே உலகு",
            "transliteration": "Agara mudhala ezhuththellaam aadhi bhagavan mudhatre ulagu",
            "english": "As the letter A is the first of all letters, so the eternal God is first in the world",
            "meaning": "Just as 'A' is the foundation of all letters, God is the foundation of all existence",
            "theme": "divine_love",
            "emotions": ["grateful", "reverent", "contemplative"]
        },
        {
            "number": 25,
            "tamil": "அன்பும் அறனும் உடைத்தாயின் இல்வாழ்க்கை பண்பும் பயனும் அது",
            "transliteration": "Anbum aranum udaitthaayin ilvaazhkkai panbum payanum adu",
            "english": "If love and virtue dwell in the heart, domestic life will be blessed with beauty and fruit",
            "meaning": "A household filled with love and righteousness brings beauty and prosperity",
            "theme": "family_love",
            "emotions": ["loving", "grateful", "content"]
        }
    ],
    "friendship": [
        {
            "number": 781,
            "tamil": "சிற்றினம் அஞ்சும் பெருமை சிறுமைதான் சுற்றமாச் சூழ்ந்து விடும்",
            "transliteration": "Sitrinam anjum perumai sirumaithaan sutramaach soozhnthu vidum",
            "english": "Greatness fears not evil company; meanness will be surrounded by it",
            "meaning": "Good character avoids bad company, while poor character attracts it",
            "theme": "friendship_quality",
            "emotions": ["wise", "cautious", "reflective"]
        },
        {
            "number": 785,
            "tamil": "நட்பிற்கு வீற்றிருக்கை யாதெனில் கொட்பிற்கும் கொள்வாரைக் கொள்வதே",
            "transliteration": "Natpirkku veetrirukkai yaadhenil kotpirkkum kollvaaraik kollvadhe",
            "english": "What is the essence of friendship? It is to choose those who will choose us in adversity",
            "meaning": "True friendship means choosing friends who will stand by us in difficult times",
            "theme": "loyalty",
            "emotions": ["loyal", "trusting", "grateful"]
        }
    ],
    "wisdom": [
        {
            "number": 423,
            "tamil": "எப்பொருள் யார்யார்வாய்க் கேட்பினும் அப்பொருள் மெய்ப்பொருள் காண்பது அறிவு",
            "transliteration": "Epporul yaar yaarvaaik ketpinum apporul meypporul kaanpadhu arivu",
            "english": "Whatever be the source, whatever be the speaker, to grasp the truth is wisdom",
            "meaning": "True wisdom is the ability to discern truth regardless of who speaks it",
            "theme": "discernment",
            "emotions": ["wise", "thoughtful", "open_minded"]
        },
        {
            "number": 426,
            "tamil": "எண்ணிய எண்ணியாங்கு எய்து எண்ணியார் திண்ணியர் ஆகப் பெறின்",
            "transliteration": "Enniya enniyaangu eidhu enniyaar thinniyar aagap perin",
            "english": "Whatever one thinks, that one achieves, if one's thoughts are firm",
            "meaning": "Firm determination leads to the achievement of one's goals",
            "theme": "determination",
            "emotions": ["determined", "confident", "focused"]
        }
    ],
    "ethics": [
        {
            "number": 31,
            "tamil": "செல்வத்துள் செல்வம் செவிச்செல்வம் அச்செல்வம் செல்வத்துள் எல்லாம் தலை",
            "transliteration": "Selvaththul selvan sevich selvan ach selvan selvaththul ellaam thalai",
            "english": "Among all wealth, the wealth of learning is the highest",
            "meaning": "Knowledge is the greatest of all riches",
            "theme": "education",
            "emotions": ["inspired", "motivated", "humble"]
        },
        {
            "number": 35,
            "tamil": "யாதானும் நாடாமால் ஊராமால் என்னொருவன் சாந்துணையும் கல்லாத வாறு",
            "transliteration": "Yaadhaanum naadaamaal uraamaal ennoruvan saanthunaiyum kalladha vaaru",
            "english": "What does it matter if one does not learn, even if one has all the wealth in the world?",
            "meaning": "Without learning, even great wealth is meaningless",
            "theme": "knowledge",
            "emotions": ["reflective", "humble", "motivated"]
        }
    ],
    "leadership": [
        {
            "number": 381,
            "tamil": "இறந்த மெனினும் எழுந்த மன்னோடு உறந்தாரை உள்ளாள் மகள்",
            "transliteration": "Irandha meninum ezhuntha mannodu urandhaarai ullaal magal",
            "english": "Even if dead, a king's daughter will not forget her father's friends",
            "meaning": "Loyalty to family and friends should be maintained even in difficult times",
            "theme": "loyalty",
            "emotions": ["loyal", "grateful", "respectful"]
        },
        {
            "number": 385,
            "tamil": "ஒழுக்கம் விழுப்பம் தரலான் ஒழுக்கம் உயிரினும் ஓம்பப் படும்",
            "transliteration": "Ozhukkam vizhuppam tharalaan ozhukkam uyirinum ombap padum",
            "english": "Good conduct brings esteem; therefore, good conduct should be preserved more than life",
            "meaning": "Moral character brings respect and should be valued more than life itself",
            "theme": "integrity",
            "emotions": ["principled", "respectful", "determined"]
        }
    ],
    "wealth": [
        {
            "number": 751,
            "tamil": "பொருளல்ல வற்றைப் பொருளென்று உணரும் மருளானாம் மாளாத உள்ளம்",
            "transliteration": "Porulalla vatraip porulendru unarum marulaanaam maalaadha ullam",
            "english": "The mind that considers what is not wealth as wealth is deluded",
            "meaning": "True wealth is not material possessions but virtues and wisdom",
            "theme": "true_wealth",
            "emotions": ["wise", "content", "reflective"]
        },
        {
            "number": 755,
            "tamil": "இலமென்று அசைஇ இருப்பாரைக் காணின் நிலமென்னும் நல்லாள் நகும்",
            "transliteration": "Ilamendru asai iruppaaraik kaanin nilamennum nallaal nagum",
            "english": "When one sees those who say 'I have nothing' and remain idle, the goddess of wealth laughs",
            "meaning": "Wealth comes to those who work hard, not to those who are lazy",
            "theme": "hard_work",
            "emotions": ["motivated", "determined", "inspired"]
        }
    ],
    "forgiveness": [
        {
            "number": 152,
            "tamil": "ஒறுத்தார்க்கு ஒருநாளை இன்பம் பொறுத்தார்க்குப் பொன்றும் துணையும் புகழ்",
            "transliteration": "Otruththaarkku orunaalai inbam poruththaarkkup ponrum thunaiyum pugazh",
            "english": "The pleasure of those who punish lasts for a day; the fame of those who forgive lasts till the end of time",
            "meaning": "Forgiveness brings lasting fame and peace, while punishment brings only temporary satisfaction",
            "theme": "forgiveness",
            "emotions": ["peaceful", "wise", "compassionate"]
        }
    ],
    "patience": [
        {
            "number": 156,
            "tamil": "தன்னை உணர்த்தினான் தம்மை இன்அறுத்தான் தன்னுடையான் வேண்டின் உணர்",
            "transliteration": "Thannai unarththinaan thammai inaruththaan thannudaiyaan vendin unar",
            "english": "He who has patience will have what he wants; he who has no patience will have what he does not want",
            "meaning": "Patience leads to achieving one's goals, while impatience leads to failure",
            "theme": "patience",
            "emotions": ["patient", "determined", "calm"]
        }
    ]
}

# Emotion keywords mapping
EMOTION_KEYWORDS = {
    "sad": ["sad", "depressed", "lonely", "heartbroken", "grief", "sorrow", "pain", "hurt", "crying", "tears"],
    "angry": ["angry", "furious", "rage", "hate", "resentment", "bitter", "hostile", "irritated", "annoyed"],
    "confused": ["confused", "uncertain", "doubt", "question", "why", "how", "what", "unsure", "puzzled"],
    "grateful": ["thankful", "grateful", "blessed", "appreciate", "gratitude", "thank", "blessing"],
    "love": ["love", "romance", "relationship", "marriage", "family", "care", "affection", "heart"],
    "wisdom": ["wisdom", "knowledge", "learn", "teach", "understand", "truth", "philosophy", "meaning"],
    "fear": ["fear", "afraid", "scared", "anxiety", "worry", "nervous", "terrified", "panic"],
    "joy": ["happy", "joy", "excited", "celebrate", "success", "achievement", "victory", "triumph"],
    "peaceful": ["peaceful", "calm", "serene", "tranquil", "forgiving", "compassionate", "merciful"],
    "patient": ["patient", "tolerant", "enduring", "persevering", "waiting", "steady"]
}

# Theme keywords mapping
THEME_KEYWORDS = {
    "love": ["love", "romance", "marriage", "relationship", "family", "heart", "affection"],
    "friendship": ["friend", "friendship", "companion", "ally", "buddy", "mate"],
    "wisdom": ["wisdom", "knowledge", "learn", "teach", "understand", "truth"],
    "ethics": ["right", "wrong", "moral", "ethical", "good", "bad", "virtue", "sin"],
    "leadership": ["leader", "king", "ruler", "govern", "manage", "authority", "power"],
    "wealth": ["money", "wealth", "rich", "poor", "poverty", "fortune", "prosperity"],
    "forgiveness": ["forgive", "forgiveness", "pardon", "excuse", "mercy", "compassion"],
    "patience": ["patience", "patient", "wait", "endure", "persevere", "tolerance"]
}

def detect_emotion(text):
    """Detect emotion from user input"""
    text_lower = text.lower()
    detected_emotions = []
    
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                detected_emotions.append(emotion)
                break
    
    # Use TextBlob for sentiment analysis as backup
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    
    if not detected_emotions:
        if sentiment > 0.3:
            detected_emotions.append("joy")
        elif sentiment < -0.3:
            detected_emotions.append("sad")
        else:
            detected_emotions.append("neutral")
    
    return detected_emotions[:2]  # Return top 2 emotions

def detect_theme(text):
    """Detect theme from user input"""
    text_lower = text.lower()
    detected_themes = []
    
    for theme, keywords in THEME_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                detected_themes.append(theme)
                break
    
    return detected_themes[:2] if detected_themes else ["wisdom"]

def find_relevant_kurals(emotions, themes):
    """Find relevant Kurals based on emotions and themes"""
    relevant_kurals = []
    
    # Search in themes first
    for theme in themes:
        if theme in KURAL_DATABASE:
            relevant_kurals.extend(KURAL_DATABASE[theme])
    
    # If no theme matches, search by emotions
    if not relevant_kurals:
        for theme, kurals in KURAL_DATABASE.items():
            for kural in kurals:
                if any(emotion in kural.get("emotions", []) for emotion in emotions):
                    relevant_kurals.append(kural)
    
    # If still no matches, return wisdom kurals
    if not relevant_kurals:
        relevant_kurals = KURAL_DATABASE.get("wisdom", [])
    
    return relevant_kurals[:3]  # Return top 3 kurals

def display_kural(kural, index=0):
    """Display a Kural in a beautiful card format"""
    st.markdown(f"""
    <div class="kural-card">
        <h3>Kural #{kural['number']}</h3>
        <p><strong>Tamil:</strong> {kural['tamil']}</p>
        <p><strong>Transliteration:</strong> {kural['transliteration']}</p>
        <p><strong>English:</strong> {kural['english']}</p>
        <p><strong>Meaning:</strong> {kural['meaning']}</p>
        <p><strong>Theme:</strong> {kural['theme'].replace('_', ' ').title()}</p>
    </div>
    """, unsafe_allow_html=True)

def get_moral_reflection(emotions, themes):
    """Generate a moral reflection based on emotions and themes"""
    reflections = {
        "sad": "In moments of sorrow, remember that every difficulty is a teacher. The ancient wisdom reminds us that pain often leads to growth and understanding.",
        "angry": "Anger clouds judgment and wisdom. The sages teach us that patience and forgiveness are the paths to inner peace and true strength.",
        "confused": "Confusion is the beginning of wisdom. When we question, we open ourselves to learning. Trust that clarity will come with time and reflection.",
        "grateful": "Gratitude is the foundation of a happy life. When we appreciate what we have, we attract more blessings and find contentment in simplicity.",
        "love": "Love is the greatest force in the universe. It heals, transforms, and connects us all. Cherish and nurture the love in your heart.",
        "wisdom": "True wisdom comes from experience, reflection, and an open heart. Seek knowledge not just for yourself, but to help others on their journey.",
        "fear": "Fear is often a sign that we're stepping into growth. Courage is not the absence of fear, but the willingness to move forward despite it.",
        "joy": "Joy is a gift to be shared. When we spread happiness, we multiply it. Let your light shine and inspire others to find their own joy.",
        "peaceful": "Peace is not the absence of problems, but the ability to deal with them calmly. Inner peace is the greatest treasure we can cultivate.",
        "patient": "Patience is the companion of wisdom. Great things take time to grow, and the most beautiful transformations happen gradually."
    }
    
    if emotions:
        return reflections.get(emotions[0], "Every experience, whether pleasant or challenging, offers us an opportunity to grow and learn.")
    return "Life is a journey of learning and growth. Each moment teaches us something valuable if we're open to receiving it."

# Main app
def main():
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## 🌟 KuralCompanion")
        selected = option_menu(
            menu_title=None,
            options=["Home", "Ask Kural", "Explore Themes", "About"],
            icons=["house", "question-circle", "book", "info-circle"],
            menu_icon="cast",
            default_index=0,
        )
    
    if selected == "Home":
        st.markdown('<h1 class="main-header">🌟 KuralCompanion</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Ancient Wisdom for Modern Life</p>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            ### Welcome to Your Digital Sage
            
            KuralCompanion is your guide to the timeless wisdom of Thiruvalluvar's Thirukkural. 
            Whether you're seeking advice, expressing emotions, or exploring life's deeper questions, 
            let the ancient verses illuminate your path.
            
            **How it works:**
            - Share your thoughts, feelings, or questions
            - Our AI detects your emotions and themes
            - Receive relevant Thirukkural verses with meanings
            - Get gentle moral reflections for guidance
            
            Start your journey by asking a question or sharing how you feel!
            """)
            
            if st.button("🚀 Start Your Journey", type="primary"):
                st.switch_page("Ask Kural")
    
    elif selected == "Ask Kural":
        st.markdown('<h1 class="main-header">💭 Ask Kural</h1>', unsafe_allow_html=True)
        
        # User input
        user_input = st.text_area(
            "Share your thoughts, feelings, or questions...",
            placeholder="e.g., 'I'm feeling sad about losing my job' or 'Why do people hurt others?' or 'I'm grateful for my family'",
            height=100
        )
        
        if st.button("🌟 Find Wisdom", type="primary") and user_input:
            with st.spinner("Analyzing your words and finding relevant wisdom..."):
                # Detect emotions and themes
                emotions = detect_emotion(user_input)
                themes = detect_theme(user_input)
                
                # Display detected emotions and themes
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🎭 Detected Emotions")
                    for emotion in emotions:
                        st.markdown(f'<span class="emotion-badge emotion-{emotion}">{emotion.title()}</span>', unsafe_allow_html=True)
                
                with col2:
                    st.subheader("📚 Detected Themes")
                    for theme in themes:
                        st.markdown(f'<span class="emotion-badge emotion-wisdom">{theme.title()}</span>', unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Find and display relevant Kurals
                relevant_kurals = find_relevant_kurals(emotions, themes)
                
                st.subheader("📖 Relevant Thirukkural Verses")
                for i, kural in enumerate(relevant_kurals):
                    display_kural(kural, i)
                
                # Moral reflection
                st.markdown("---")
                st.subheader("💡 Moral Reflection")
                reflection = get_moral_reflection(emotions, themes)
                st.info(reflection)
                
                # Conversation mode
                st.markdown("---")
                st.subheader("🤖 Conversational AI Mode")
                st.markdown("""
                **Your Question:** "{}"
                
                **KuralCompanion's Response:** Based on your emotions and themes, here are the relevant verses from Thirukkural that speak to your situation. 
                Remember, every challenge is an opportunity for growth, and every question leads to wisdom.
                """.format(user_input))
    
    elif selected == "Explore Themes":
        st.markdown('<h1 class="main-header">📚 Explore Themes</h1>', unsafe_allow_html=True)
        
        # Theme selection
        theme_options = list(KURAL_DATABASE.keys())
        selected_theme = st.selectbox("Choose a theme to explore:", theme_options)
        
        if selected_theme:
            st.subheader(f"📖 {selected_theme.title()} - Thirukkural Verses")
            
            for kural in KURAL_DATABASE[selected_theme]:
                display_kural(kural)
                
                # Add some spacing
                st.markdown("<br>", unsafe_allow_html=True)
    
    elif selected == "About":
        st.markdown('<h1 class="main-header">ℹ️ About KuralCompanion</h1>', unsafe_allow_html=True)
        
        st.markdown("""
        ### 🌟 Vision Statement
        
        **"Ancient Wisdom for Modern Life"**
        
        A digital sage that listens, understands, and gently guides—through the eternal words of Thiruvalluvar.
        
        ### 🎯 Core Features
        
        **Emotion-to-Kural Mapping**
        - Detects intent, emotion, and theme from your input
        - Maps to relevant Thirukkural verses
        - Provides contextual meanings and reflections
        
        **Conversational AI Mode**
        - Interactive dialogue with ancient wisdom
        - Personalized guidance based on your situation
        - Gentle moral reflections for modern challenges
        
        ### 📖 About Thirukkural
        
        Thirukkural is a classic Tamil text consisting of 1,330 couplets dealing with the everyday virtues of an individual. 
        It is one of the most important works in Tamil literature and is considered a masterpiece of ethical literature.
        
        The text is divided into three sections:
        - **Aram (Virtue)** - 380 verses on moral values
        - **Porul (Wealth)** - 700 verses on political and economic matters  
        - **Inbam (Love)** - 250 verses on human love and relationships
        
        ### 🚀 Technology
        
        Built with Streamlit, Python, and AI-powered emotion detection to bridge ancient wisdom with modern technology.
        """)

if __name__ == "__main__":
    main()