import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from textblob import TextBlob
import re
from collections import defaultdict
import json
from streamlit_option_menu import option_menu
from kural_database import KURAL_DATABASE, EMOTION_KEYWORDS, THEME_KEYWORDS, get_all_kurals, get_kural_by_number, get_kurals_by_theme, get_kurals_by_emotion, search_kurals_by_keyword
from comprehensive_kurals import ADDITIONAL_KURALS, merge_kural_databases
from extended_kurals import EXTENDED_KURALS, merge_all_kural_databases

# Create comprehensive database by merging all three databases for maximum coverage
COMPREHENSIVE_KURAL_DATABASE = merge_all_kural_databases(KURAL_DATABASE, ADDITIONAL_KURALS, EXTENDED_KURALS)

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

# Thirukkural Database is now imported from kural_database.py

# Emotion and Theme keywords are now imported from kural_database.py

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
    """Find relevant Kurals based on detected emotions and themes with robust matching"""
    # Normalize inputs
    detected_emotions = [e.lower() for e in emotions if e.lower() != "neutral"]
    detected_themes = [t.lower() for t in themes]

    def search_in_comprehensive(keyword: str):
        """Keyword search across the comprehensive database (english, meaning, tamil, theme)."""
        matches = []
        key_lower = keyword.lower()
        for db_theme, kurals in COMPREHENSIVE_KURAL_DATABASE.items():
            for k in kurals:
                tamil_text = f"{k.get('line1', '')} {k.get('line2', '')}".strip()
                if (
                    key_lower in k.get("english", "").lower()
                    or key_lower in k.get("meaning", "").lower()
                    or key_lower in tamil_text.lower()
                    or key_lower in k.get("theme", "").lower()
                ):
                    matches.append(k)
        return matches

    # Collect candidates with a simple scoring approach
    scored = []  # (score, kural)

    # 1) Theme-based: case-insensitive and fuzzy match against database theme names
    db_items = list(COMPREHENSIVE_KURAL_DATABASE.items())
    for db_theme, kurals in db_items:
        db_theme_lower = db_theme.lower()
        theme_match_strength = 0
        for t in detected_themes:
            if t == db_theme_lower:
                theme_match_strength = max(theme_match_strength, 2)
            elif t in db_theme_lower:
                theme_match_strength = max(theme_match_strength, 1)

        if theme_match_strength > 0:
            for k in kurals:
                scored.append((2 + theme_match_strength, k))

    # 2) Theme-keyword fallback: use THEME_KEYWORDS to find related words in content
    for t in detected_themes:
        related_keywords = THEME_KEYWORDS.get(t, [t])
        for kw in related_keywords[:5]:  # limit for efficiency
            for k in search_in_comprehensive(kw):
                scored.append((2, k))

    # 3) Emotion-based: match detected emotions with kural emotions (case-insensitive)
    if detected_emotions:
        for _, kurals in db_items:
            for k in kurals:
                k_emotions = [str(e).lower() for e in k.get("emotions", [])]
                if any(e in k_emotions for e in detected_emotions):
                    # Slightly lower weight than strong theme match
                    scored.append((1, k))

    # 4) Emotion keyword fallback: search text with emotion words
    for e in detected_emotions:
        for k in search_in_comprehensive(e):
            scored.append((1, k))

    # If nothing scored yet, fallback to first available theme's kurals
    if not scored and db_items:
        first_theme_kurals = next(iter(db_items))[1]
        for k in first_theme_kurals:
            scored.append((0, k))

    # Deduplicate by kural number and sort by score (desc), preserving stability
    seen = set()
    unique_scored = []
    for score, k in sorted(scored, key=lambda x: x[0], reverse=True):
        num = k.get("number")
        if num not in seen:
            seen.add(num)
            unique_scored.append((score, k))

    return [k for _, k in unique_scored][:2]

def get_total_kural_count():
    """Get the total number of kurals in the comprehensive database"""
    total_count = 0
    for theme, kurals in COMPREHENSIVE_KURAL_DATABASE.items():
        total_count += len(kurals)
    return total_count

def get_theme_counts():
    """Get the count of kurals for each theme"""
    theme_counts = {}
    for theme, kurals in COMPREHENSIVE_KURAL_DATABASE.items():
        theme_counts[theme] = len(kurals)
    return theme_counts

def display_kural(kural, index=0, show_transliteration: bool = True, show_english: bool = True):
    """Display a Kural card. Tamil is always shown. Transliteration/English are optional."""
    
    # Format Tamil text in two lines
    tamil_text = f"{kural.get('line1', '')}<br>{kural.get('line2', '')}" if 'line1' in kural else kural['tamil']
    
    # Use common transliteration preference from session state
    show_translit = st.session_state.get('show_transliteration', True)
    
    # Format transliteration in two lines (only if selected)
    transliteration_text = ""
    if show_translit:
        transliteration_parts = kural['transliteration'].split(' ', 1)
        transliteration_text = (
            f"{transliteration_parts[0]}<br>{transliteration_parts[1]}" if len(transliteration_parts) > 1 else kural['transliteration']
        )
    
    # Get Tamil explanations
    mv = kural.get('mv', '')
    sp = kural.get('sp', '')
    mk = kural.get('mk', '')
    
    # Create explanations section using common preference from session state
    explanations_html = ""
    if mv or sp or mk:
        explanations_html = "<p><strong>Tamil Explanations:</strong></p>"
        
        # Use the selected explanation from session state
        selected_key = st.session_state.get('selected_explanation')
        if selected_key == 'mv' and mv:
            explanations_html += f"<p><em>மு.வரதராசனார்:</em> {mv}</p>"
        elif selected_key == 'sp' and sp:
            explanations_html += f"<p><em>சாலமன் பாப்பையா:</em> {sp}</p>"
        elif selected_key == 'mk' and mk:
            explanations_html += f"<p><em>மு.கருணாநிதி:</em> {mk}</p>"
        else:
            # Fallback: show first available explanation
            if mv:
                explanations_html += f"<p><em>மு.வரதராசனார்:</em> {mv}</p>"
            elif sp:
                explanations_html += f"<p><em>சாலமன் பாப்பையா:</em> {sp}</p>"
            elif mk:
                explanations_html += f"<p><em>மு.கருணாநிதி:</em> {mk}</p>"
    
    # Build conditional sections
    sections_html = [
        f"<p><strong>Tamil:</strong><br>{tamil_text}</p>"
    ]
    if show_translit and transliteration_text:
        sections_html.append(f"<p><strong>Transliteration:</strong><br>{transliteration_text}</p>")
    if show_english:
        sections_html.append(f"<p><strong>English:</strong> {kural['english']}</p>")
    sections_html.append(f"<p><strong>Meaning:</strong> {kural['meaning']}</p>")
    if explanations_html:
        sections_html.append(explanations_html)
    sections_html.append(f"<p><strong>Theme:</strong> {kural['theme'].replace('_', ' ').title()}</p>")

    st.markdown(
        f"""
        <div class="kural-card">
            <h3>Kural #{kural['number']}</h3>
            {''.join(sections_html)}
        </div>
        """,
        unsafe_allow_html=True,
    )

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
    # Initialize session state for navigation
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "Home"
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## 🌟 KuralCompanion")
        sidebar_selected = option_menu(
            menu_title=None,
            options=["Home", "Ask Kural", "Explore Themes", "About"],
            icons=["house", "question-circle", "book", "info-circle"],
            menu_icon="cast",
            default_index=0,
        )
    
    # Determine which page to show
    # If sidebar was clicked, use sidebar selection
    # If button was clicked, use session state
    if 'last_sidebar_selection' not in st.session_state:
        st.session_state.last_sidebar_selection = sidebar_selected
    
    # Check if sidebar selection changed (user clicked sidebar)
    if sidebar_selected != st.session_state.last_sidebar_selection:
        st.session_state.selected_page = sidebar_selected
        st.session_state.last_sidebar_selection = sidebar_selected
    
    selected = st.session_state.selected_page
    
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
                st.session_state.selected_page = "Ask Kural"
                st.rerun()
    
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
                
                # Conversation mode - Moved above the verses
                st.subheader("🤖 Conversational AI Mode")
                st.markdown("""
                **Your Question:** "{}"
                
                **KuralCompanion's Response:** Based on your emotions and themes, here are the relevant verses from Thirukkural that speak to your situation. 
                Remember, every challenge is an opportunity for growth, and every question leads to wisdom.
                """.format(user_input))
                
                # Moral reflection
                st.markdown("---")
                st.subheader("💡 Moral Reflection")
                reflection = get_moral_reflection(emotions, themes)
                st.info(reflection)
                
                # Find and display relevant Kurals - Moved below the AI response
                st.markdown("---")
                relevant_kurals = find_relevant_kurals(emotions, themes)
                
                st.subheader("📖 Relevant Thirukkural Verses")

                # Common display controls for all kurals
                col1, col2 = st.columns(2)
                with col1:
                    show_transliteration = st.checkbox("Show Transliteration", value=True, key="common_translit")
                with col2:
                    # Get available Tamil explanations from the first kural to determine options
                    first_kural = relevant_kurals[0] if relevant_kurals else {}
                    available_explanations = []
                    if first_kural.get('mv'):
                        available_explanations.append(("மு.வரதராசனார்", 'mv'))
                    if first_kural.get('sp'):
                        available_explanations.append(("சாலமன் பாப்பையா", 'sp'))
                    if first_kural.get('mk'):
                        available_explanations.append(("மு.கருணாநிதி", 'mk'))
                    
                    if len(available_explanations) > 1:
                        selected_explanation = st.radio(
                            "Choose Tamil explanation:",
                            options=[exp[0] for exp in available_explanations],
                            key="common_explanation"
                        )
                        # Find the selected explanation key
                        selected_key = None
                        for exp_name, exp_key in available_explanations:
                            if exp_name == selected_explanation:
                                selected_key = exp_key
                                break
                        st.session_state.selected_explanation = selected_key
                    elif len(available_explanations) == 1:
                        st.session_state.selected_explanation = available_explanations[0][1]
                        st.info(f"Available: {available_explanations[0][0]}")
                    else:
                        st.session_state.selected_explanation = None
                        st.info("No Tamil explanations available")

                # Store transliteration preference in session state
                st.session_state.show_transliteration = show_transliteration

                for i, kural in enumerate(relevant_kurals):
                    display_kural(kural, i)
    
    elif selected == "Explore Themes":
        st.markdown('<h1 class="main-header">📚 Explore Themes</h1>', unsafe_allow_html=True)
        
        # Search functionality
        st.subheader("🔍 Search Kurals")
        search_option = st.radio("Search by:", ["Theme", "Keyword", "Kural Number"])
        
        if search_option == "Theme":
            # Theme selection
            theme_options = list(COMPREHENSIVE_KURAL_DATABASE.keys())
            selected_theme = st.selectbox("Choose a theme to explore:", theme_options)
            
            if selected_theme:
                st.subheader(f"📖 {selected_theme.title()} - Thirukkural Verses")
                st.info(f"Found {len(COMPREHENSIVE_KURAL_DATABASE[selected_theme])} kurals in this theme")
                
                # Common display controls for all kurals
                col1, col2 = st.columns(2)
                with col1:
                    show_transliteration = st.checkbox("Show Transliteration", value=True, key="theme_translit")
                with col2:
                    # Get available Tamil explanations from the first kural to determine options
                    theme_kurals = COMPREHENSIVE_KURAL_DATABASE[selected_theme]
                    first_kural = theme_kurals[0] if theme_kurals else {}
                    available_explanations = []
                    if first_kural.get('mv'):
                        available_explanations.append(("மு.வரதராசனார்", 'mv'))
                    if first_kural.get('sp'):
                        available_explanations.append(("சாலமன் பாப்பையா", 'sp'))
                    if first_kural.get('mk'):
                        available_explanations.append(("மு.கருணாநிதி", 'mk'))
                    
                    if len(available_explanations) > 1:
                        selected_explanation = st.radio(
                            "Choose Tamil explanation:",
                            options=[exp[0] for exp in available_explanations],
                            key="theme_explanation"
                        )
                        # Find the selected explanation key
                        selected_key = None
                        for exp_name, exp_key in available_explanations:
                            if exp_name == selected_explanation:
                                selected_key = exp_key
                                break
                        st.session_state.selected_explanation = selected_key
                    elif len(available_explanations) == 1:
                        st.session_state.selected_explanation = available_explanations[0][1]
                        st.info(f"Available: {available_explanations[0][0]}")
                    else:
                        st.session_state.selected_explanation = None
                        st.info("No Tamil explanations available")

                # Store transliteration preference in session state
                st.session_state.show_transliteration = show_transliteration
                
                for kural in theme_kurals:
                    display_kural(kural)
                    st.markdown("<br>", unsafe_allow_html=True)
        
        elif search_option == "Keyword":
            keyword = st.text_input("Enter a keyword to search in kurals:")
            if keyword and st.button("Search"):
                matching_kurals = search_kurals_by_keyword(keyword)
                if matching_kurals:
                    st.subheader(f"🔍 Search Results for '{keyword}'")
                    st.info(f"Found {len(matching_kurals)} matching kurals")
                    
                    # Common display controls for all kurals
                    col1, col2 = st.columns(2)
                    with col1:
                        show_transliteration = st.checkbox("Show Transliteration", value=True, key="keyword_translit")
                    with col2:
                        # Get available Tamil explanations from the first kural to determine options
                        first_kural = matching_kurals[0] if matching_kurals else {}
                        available_explanations = []
                        if first_kural.get('mv'):
                            available_explanations.append(("மு.வரதராசனார்", 'mv'))
                        if first_kural.get('sp'):
                            available_explanations.append(("சாலமன் பாப்பையா", 'sp'))
                        if first_kural.get('mk'):
                            available_explanations.append(("மு.கருணாநிதி", 'mk'))
                        
                        if len(available_explanations) > 1:
                            selected_explanation = st.radio(
                                "Choose Tamil explanation:",
                                options=[exp[0] for exp in available_explanations],
                                key="keyword_explanation"
                            )
                            # Find the selected explanation key
                            selected_key = None
                            for exp_name, exp_key in available_explanations:
                                if exp_name == selected_explanation:
                                    selected_key = exp_key
                                    break
                            st.session_state.selected_explanation = selected_key
                        elif len(available_explanations) == 1:
                            st.session_state.selected_explanation = available_explanations[0][1]
                            st.info(f"Available: {available_explanations[0][0]}")
                        else:
                            st.session_state.selected_explanation = None
                            st.info("No Tamil explanations available")

                    # Store transliteration preference in session state
                    st.session_state.show_transliteration = show_transliteration
                    
                    for kural in matching_kurals:
                        display_kural(kural)
                        st.markdown("<br>", unsafe_allow_html=True)
                else:
                    st.warning(f"No kurals found matching '{keyword}'")
        
        elif search_option == "Kural Number":
            kural_number = st.number_input("Enter Kural number (1-1330):", min_value=1, max_value=1330, value=1)
            if st.button("Find Kural"):
                kural = get_kural_by_number(kural_number)
                if kural:
                    st.subheader(f"📖 Kural #{kural_number}")
                    
                    # Common display controls for the kural
                    col1, col2 = st.columns(2)
                    with col1:
                        show_transliteration = st.checkbox("Show Transliteration", value=True, key="number_translit")
                    with col2:
                        # Get available Tamil explanations from the kural
                        available_explanations = []
                        if kural.get('mv'):
                            available_explanations.append(("மு.வரதராசனார்", 'mv'))
                        if kural.get('sp'):
                            available_explanations.append(("சாலமன் பாப்பையா", 'sp'))
                        if kural.get('mk'):
                            available_explanations.append(("மு.கருணாநிதி", 'mk'))
                        
                        if len(available_explanations) > 1:
                            selected_explanation = st.radio(
                                "Choose Tamil explanation:",
                                options=[exp[0] for exp in available_explanations],
                                key="number_explanation"
                            )
                            # Find the selected explanation key
                            selected_key = None
                            for exp_name, exp_key in available_explanations:
                                if exp_name == selected_explanation:
                                    selected_key = exp_key
                                    break
                            st.session_state.selected_explanation = selected_key
                        elif len(available_explanations) == 1:
                            st.session_state.selected_explanation = available_explanations[0][1]
                            st.info(f"Available: {available_explanations[0][0]}")
                        else:
                            st.session_state.selected_explanation = None
                            st.info("No Tamil explanations available")

                    # Store transliteration preference in session state
                    st.session_state.show_transliteration = show_transliteration
                    
                    display_kural(kural)
                else:
                    st.warning(f"Kural #{kural_number} not found in the current database")
        
        # Database statistics
        st.markdown("---")
        st.subheader("📊 Database Statistics")
        total_kurals = get_total_kural_count()
        theme_counts = get_theme_counts()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Kurals", total_kurals)
        with col2:
            st.metric("Themes", len(theme_counts))
        with col3:
            st.metric("Coverage", f"{(total_kurals/1330)*100:.1f}%")
    
    elif selected == "About":
        st.markdown('<h1 class="main-header">ℹ️ About KuralCompanion</h1>', unsafe_allow_html=True)
        
        # Database Statistics
        total_kurals = get_total_kural_count()
        theme_counts = get_theme_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Kurals in Database", total_kurals)
            st.metric("Themes Covered", len(theme_counts))
        
        with col2:
            st.metric("Target Goal", "1,330 Kurals")
            st.metric("Coverage", f"{(total_kurals/1330)*100:.1f}%")
        
        # Theme breakdown
        st.subheader("📊 Database Coverage by Theme")
        theme_data = pd.DataFrame(list(theme_counts.items()), columns=['Theme', 'Count'])
        fig = px.bar(theme_data, x='Theme', y='Count', title='Kurals per Theme')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        ### 🌟 Vision Statement
        
        **"Ancient Wisdom for Modern Life"**
        
        A digital sage that listens, understands, and gently guides—through the eternal words of Thiruvalluvar.
        
        ### 🎯 Core Features
        
        **Enhanced Kural Database**
        - Comprehensive collection of Thirukkural verses
        - Organized by themes and emotions for intelligent matching
        - Multiple database files for better organization and scalability
        
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
        
        ### 📁 Database Structure
        
        The Kural database is organized into multiple files for better maintainability:
        - `kural_database.py` - Main database with core kurals
        - `comprehensive_kurals.py` - Additional kurals for extended coverage
        - `extended_kurals.py` - Further kurals for maximum coverage
        
        This modular approach allows for easy expansion and maintenance of the database.
        """)

if __name__ == "__main__":
    main()