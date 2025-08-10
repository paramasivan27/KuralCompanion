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

def find_relevant_kurals_rag(user_input, emotions, themes):
    """Find relevant Kurals using enhanced RAG approach - searching across multiple fields for better relevance"""
    # Normalize inputs
    detected_emotions = [e.lower() for e in emotions if e.lower() != "neutral"]
    detected_themes = [t.lower() for t in themes]
    
    # Create search query from user input - improved tokenization
    search_terms = [term.lower().strip() for term in user_input.lower().split() if len(term.strip()) > 2]
    
    scored = []  # (score, kural, match_details)
    
    # Search across the comprehensive database
    for db_theme, kurals in COMPREHENSIVE_KURAL_DATABASE.items():
        for kural in kurals:
            score = 0
            match_details = []
            
            # 1. Theme-based scoring (highest priority)
            db_theme_lower = db_theme.lower()
            for theme in detected_themes:
                if theme == db_theme_lower:
                    score += 15  # Exact theme match (increased from 10)
                    match_details.append(f"Exact theme match: {db_theme}")
                elif theme in db_theme_lower or db_theme_lower in theme:
                    score += 12   # Partial theme match (increased from 8)
                    match_details.append(f"Partial theme match: {db_theme}")
            
            # 2. Emotion-based scoring (enhanced)
            kural_emotions = [str(e).lower() for e in kural.get("emotions", [])]
            for emotion in detected_emotions:
                if emotion in kural_emotions:
                    score += 8   # Emotion match (increased from 6)
                    match_details.append(f"Emotion match: {emotion}")
                # Check for emotional context in meaning and english fields
                elif (emotion in kural.get("meaning", "").lower() or emotion in kural.get("english", "").lower()):
                    score += 4   # Emotional context match
                    match_details.append(f"Emotional context: {emotion}")
            
            # 3. Enhanced Content-based scoring (RAG approach)
            # Search in English field with improved matching
            english_text = kural.get("english", "").lower()
            english_matches = []
            english_score = 0
            for term in search_terms:
                if term in english_text:
                    # Boost score for longer/more meaningful terms
                    term_weight = min(len(term), 5)  # Cap at 5 for very long terms
                    english_score += term_weight
                    english_matches.append(term)
            if english_matches:
                score += english_score
                match_details.append(f"English matches: {', '.join(english_matches)}")
            
            # Search in meaning field with improved matching
            meaning_text = kural.get("meaning", "").lower()
            meaning_matches = []
            meaning_score = 0
            for term in search_terms:
                if term in meaning_text:
                    # Boost score for longer/more meaningful terms
                    term_weight = min(len(term), 5)  # Cap at 5 for very long terms
                    meaning_score += term_weight
                    meaning_matches.append(term)
            if meaning_matches:
                score += meaning_score
                match_details.append(f"Meaning matches: {', '.join(meaning_matches)}")
            
            # Search in couplet field with improved matching
            couplet_text = kural.get("couplet", "").lower()
            couplet_matches = []
            couplet_score = 0
            for term in search_terms:
                if term in couplet_text:
                    # Boost score for longer/more meaningful terms
                    term_weight = min(len(term), 4)  # Slightly lower weight for couplet
                    couplet_score += term_weight
                    couplet_matches.append(term)
            if couplet_matches:
                score += couplet_score
                match_details.append(f"Couplet matches: {', '.join(couplet_matches)}")
            
            # 4. Enhanced Contextual relevance scoring
            if score > 0:
                # Additional boost for comprehensive matches
                if len(match_details) >= 4:
                    score += 5  # Increased from 2
                elif len(match_details) >= 3:
                    score += 3  # Increased from 2
                
                # Boost for exact theme match with content matches
                if any("Exact theme match" in detail for detail in match_details):
                    if any("English matches" in detail or "Meaning matches" in detail for detail in match_details):
                        score += 5  # Increased from 3
                
                # Boost for emotional alignment with content
                if any("Emotion match" in detail for detail in match_details):
                    if any("English matches" in detail or "Meaning matches" in detail for detail in match_details):
                        score += 3
            
            # Only include kurals with meaningful scores
            if score >= 5:  # Increased minimum threshold from 3
                scored.append((score, kural, match_details))
    
    # Sort by score (descending) and return top results with match details
    scored.sort(key=lambda x: x[0], reverse=True)
    return [(kural, details) for _, kural, details in scored[:5]]  # Return top 5 with details (increased from 3)

def find_kurals_by_keywords(keywords):
    """Find relevant Kurals based on keywords using enhanced RAG approach"""
    # Normalize input
    search_keywords = [kw.lower().strip() for kw in keywords.split() if kw.strip()]
    
    if not search_keywords:
        return []
    
    # Use the RAG approach for better results
    # Create a mock user input and detect emotions/themes
    mock_input = " ".join(search_keywords)
    emotions = detect_emotion(mock_input)
    themes = detect_theme(mock_input)
    
    # Use the enhanced RAG function
    relevant_kurals_with_details = find_relevant_kurals_rag(mock_input, emotions, themes)
    
    # Return just the kurals (without details) for backward compatibility
    return [kural for kural, _ in relevant_kurals_with_details]

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
    
    # Use passed parameter instead of session state
    show_translit = show_transliteration
    
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
    
    # Create explanations section using the selected explanation preference
    explanations_html = ""
    if mv or sp or mk:
        explanations_html = "<p><strong>Tamil Explanations:</strong></p>"
        
        # Use the selected explanation from session state or fallback to first available
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

def generate_contextual_response(user_input, emotions, themes, kurals_with_details):
    """Generate an enhanced contextual response based on user input, emotions, themes, and found kurals using RAG insights"""
    response_parts = []
    
    # Start with emotional acknowledgment and empathy
    if emotions:
        if "sad" in emotions or "depressed" in emotions:
            response_parts.append("I sense you're going through a difficult time. The ancient wisdom of Thirukkural offers profound guidance for moments like these, helping us find strength and perspective.")
        elif "angry" in emotions or "frustrated" in emotions:
            response_parts.append("I understand you're feeling frustrated. Thirukkural provides timeless wisdom on managing emotions and finding inner peace through patience and understanding.")
        elif "grateful" in emotions or "joy" in emotions:
            response_parts.append("It's wonderful that you're feeling grateful. Thirukkural celebrates these positive emotions and guides us to cultivate them further, spreading joy to others.")
        elif "confused" in emotions or "uncertain" in emotions:
            response_parts.append("When facing uncertainty, Thirukkural's timeless wisdom can help clarify your path forward. Sometimes the answers we seek are found in ancient guidance.")
        elif "love" in emotions:
            response_parts.append("Love is a beautiful emotion that Thirukkural deeply explores and celebrates. It's the foundation of all meaningful relationships and personal growth.")
        elif "fear" in emotions:
            response_parts.append("Fear is a natural human emotion. Thirukkural offers wisdom on facing fears with courage and wisdom, transforming them into opportunities for growth.")
        else:
            response_parts.append("Your emotional state resonates with the wisdom contained in Thirukkural. These ancient verses have guidance for every human experience.")
    
    # Add theme context with more depth
    if themes:
        if len(themes) == 1:
            theme_response = f"The theme of {themes[0]} is deeply explored in these ancient verses, offering practical wisdom for modern life."
        else:
            theme_response = f"The themes of {', '.join(themes[:-1])} and {themes[-1]} are beautifully interconnected in Thirukkural, providing comprehensive guidance."
        response_parts.append(theme_response)
    
    # Add intelligent kural-specific insights based on RAG results
    if kurals_with_details:
        kural_numbers = [kural.get('number', 'Unknown') for kural, _ in kurals_with_details]
        match_details = [details for _, details in kurals_with_details]
        
        if len(kural_numbers) == 1:
            response_parts.append(f"I've found Kural #{kural_numbers[0]}, which directly addresses your situation with remarkable precision.")
        else:
            response_parts.append(f"I've found {len(kural_numbers)} highly relevant kurals (#{', '.join(map(str, kural_numbers))}) that directly address your situation.")
        
        # Add insights about why these kurals are relevant
        response_parts.append("These verses were selected because they match your emotional state, address your themes, and contain content that directly relates to your question.")
        
        # Add specific insights about the matches if available
        if match_details:
            unique_matches = set()
            for details in match_details:
                for detail in details:
                    if "match" in detail.lower():
                        unique_matches.add(detail.split(":")[0].strip())
            
            if unique_matches:
                match_insights = f"The relevance comes from {', '.join(list(unique_matches)[:3])}."
                response_parts.append(match_insights)
    
    # Add personalized guidance based on the context
    if emotions and any(emotion in ["sad", "angry", "confused", "fear"] for emotion in emotions):
        response_parts.append("Remember, every challenge is an opportunity for growth, and every question leads to wisdom. Thirukkural teaches us that difficulties are temporary, but the lessons we learn from them are eternal.")
    elif emotions and any(emotion in ["joy", "grateful", "love"] for emotion in emotions):
        response_parts.append("Your positive emotions are a gift to be shared. Thirukkural encourages us to spread these feelings and use them as a foundation for helping others.")
    else:
        response_parts.append("Thirukkural's wisdom is timeless because it addresses the fundamental aspects of human experience that remain constant across generations.")
    
    return ' '.join(response_parts)

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
            options=["Home", "Ask Kural", "Know About Kural", "Explore Themes", "About"],
            icons=["house", "question-circle", "lightbulb", "book", "info-circle"],
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
            - Our enhanced RAG system analyzes your input across multiple dimensions
            - AI detects emotions, themes, and contextual relevance
            - Receive highly relevant Thirukkural verses with detailed explanations
            - Understand why each verse was selected for your situation
            
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
        
        # Display options - moved above the Find Wisdom button
        st.markdown("---")
        with st.expander("⚙️ Display Options", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                show_transliteration = st.checkbox("Show Transliteration", value=True, key="ask_translit")
            with col2:
                # Get available Tamil explanations from a sample kural to determine options
                # We'll use a sample from the database to show available options
                sample_kural = None
                for theme, kurals in COMPREHENSIVE_KURAL_DATABASE.items():
                    if kurals:
                        sample_kural = kurals[0]
                        break
                
                available_explanations = []
                if sample_kural:
                    if sample_kural.get('mv'):
                        available_explanations.append(("மு.வரதராசனார்", 'mv'))
                    if sample_kural.get('sp'):
                        available_explanations.append(("சாலமன் பாப்பையா", 'sp'))
                    if sample_kural.get('mk'):
                        available_explanations.append(("மு.கருணாநிதி", 'mk'))
                
                if len(available_explanations) > 1:
                    selected_explanation = st.radio(
                        "Choose Tamil explanation:",
                        options=[exp[0] for exp in available_explanations],
                        key="ask_explanation"
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
        
        if st.button("🌟 Find Wisdom", type="primary") and user_input:
            with st.spinner("Analyzing your words and finding relevant wisdom..."):
                # Detect emotions and themes
                emotions = detect_emotion(user_input)
                themes = detect_theme(user_input)
                
                # Display detected emotions and themes in collapsible sections
                col1, col2 = st.columns(2)
                
                with col1:
                    with st.expander("🎭 Detected Emotions", expanded=False):
                        for emotion in emotions:
                            st.markdown(f'<span class="emotion-badge emotion-{emotion}">{emotion.title()}</span>', unsafe_allow_html=True)
                
                with col2:
                    with st.expander("📚 Detected Themes", expanded=False):
                        for theme in themes:
                            st.markdown(f'<span class="emotion-badge emotion-wisdom">{theme.title()}</span>', unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Conversation mode - Enhanced RAG-based response
                st.subheader("🤖 Conversational AI Mode")
                
                # Find relevant Kurals first to generate better contextual response
                relevant_kurals = find_relevant_kurals_rag(user_input, emotions, themes)
                
                # Generate contextual response using the new function
                contextual_response = generate_contextual_response(user_input, emotions, themes, relevant_kurals)
                
                st.markdown(f"""
                **Your Question:** "{user_input}"
                
                **KuralCompanion's Response:** {contextual_response}
                """)
                
                # Find and display relevant Kurals using enhanced RAG approach
                st.markdown("---")
                relevant_kurals = find_relevant_kurals_rag(user_input, emotions, themes)
                
                if relevant_kurals:
                    st.subheader("📖 Relevant Thirukkural Verses")
                    st.info(f"Found {len(relevant_kurals)} highly relevant kurals using our enhanced RAG system")

                    for i, (kural, details) in enumerate(relevant_kurals):
                        # Use the display options selected by the user
                        display_kural(kural, i, show_transliteration=show_transliteration, show_english=True)
                        
                        # Enhanced match details display
                        with st.expander(f"🔍 Why this Kural is relevant (Score: {sum(1 for d in details if 'match' in d.lower())} matches)"):
                            for detail in details:
                                if "Exact theme match" in detail:
                                    st.success(f"✅ {detail}")
                                elif "Partial theme match" in detail:
                                    st.info(f"🔗 {detail}")
                                elif "Emotion match" in detail:
                                    st.warning(f"💭 {detail}")
                                elif "Emotional context" in detail:
                                    st.warning(f"💭 {detail}")
                                elif "English matches" in detail:
                                    st.success(f"📝 {detail}")
                                elif "Meaning matches" in detail:
                                    st.success(f"📖 {detail}")
                                elif "Couplet matches" in detail:
                                    st.info(f"📜 {detail}")
                                else:
                                    st.write(f"• {detail}")
                else:
                    st.warning("No relevant Kurals found for your query. Try rephrasing your question or using different keywords.")
                    st.info("💡 Tip: Try using more specific words or describing your situation in detail for better matches.")
    
    elif selected == "Know About Kural":
        st.markdown('<h1 class="main-header">💡 Know About Kural</h1>', unsafe_allow_html=True)
        
        # User input
        user_input = st.text_area(
            "Ask about any topic, concept, or subject...",
            placeholder="e.g., 'Tell me about Rain' or 'Tell me about Friendship' or 'What does Thirukkural say about Leadership?'",
            height=100
        )
        
        # Display options - similar to Ask Kural section
        st.markdown("---")
        with st.expander("⚙️ Display Options", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                show_transliteration = st.checkbox("Show Transliteration", value=True, key="know_translit")
            with col2:
                # Get available Tamil explanations from a sample kural to determine options
                sample_kural = None
                for theme, kurals in COMPREHENSIVE_KURAL_DATABASE.items():
                    if kurals:
                        sample_kural = kurals[0]
                        break
                
                available_explanations = []
                if sample_kural:
                    if sample_kural.get('mv'):
                        available_explanations.append(("மு.வரதராசனார்", 'mv'))
                    if sample_kural.get('sp'):
                        available_explanations.append(("சாலமன் பாப்பையா", 'sp'))
                if sample_kural.get('mk'):
                    available_explanations.append(("மு.கருணாநிதி", 'mk'))
                
                if len(available_explanations) > 1:
                    selected_explanation = st.radio(
                        "Choose Tamil explanation:",
                        options=[exp[0] for exp in available_explanations],
                        key="know_explanation"
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
        
        if st.button("💡 Know Thirukkural", type="primary") and user_input:
            with st.spinner("Searching for relevant wisdom using our enhanced RAG system..."):
                # Detect emotions and themes for better context
                emotions = detect_emotion(user_input)
                themes = detect_theme(user_input)
                
                # Use the enhanced RAG approach for better results
                relevant_kurals_with_details = find_relevant_kurals_rag(user_input, emotions, themes)
                
                if relevant_kurals_with_details:
                    st.markdown("---")
                    st.subheader("🤖 KuralCompanion's Response")
                    
                    # Generate contextual response using the enhanced function
                    contextual_response = generate_contextual_response(user_input, emotions, themes, relevant_kurals_with_details)
                    
                    st.markdown(f"""
                    **Your Question:** "{user_input}"
                    
                    **KuralCompanion's Response:** {contextual_response}
                    """)
                    
                    st.markdown("---")
                    st.subheader("📖 Relevant Thirukkural Verses")
                    st.info(f"Found {len(relevant_kurals_with_details)} highly relevant kurals using our enhanced RAG system")

                    for i, (kural, details) in enumerate(relevant_kurals_with_details):
                        # Use the display options selected by the user
                        display_kural(kural, i, show_transliteration=show_transliteration, show_english=True)
                        
                        # Enhanced match details display
                        with st.expander(f"🔍 Why this Kural is relevant (Score: {sum(1 for d in details if 'match' in d.lower())} matches)"):
                            for detail in details:
                                if "Exact theme match" in detail:
                                    st.success(f"✅ {detail}")
                                elif "Partial theme match" in detail:
                                    st.info(f"🔗 {detail}")
                                elif "Emotion match" in detail:
                                    st.warning(f"💭 {detail}")
                                elif "Emotional context" in detail:
                                    st.warning(f"💭 {detail}")
                                elif "English matches" in detail:
                                    st.success(f"📝 {detail}")
                                elif "Meaning matches" in detail:
                                    st.success(f"📖 {detail}")
                                elif "Couplet matches" in detail:
                                    st.info(f"📜 {detail}")
                                else:
                                    st.write(f"• {detail}")
                else:
                    st.warning("No relevant Kurals found for your query. Try using different keywords or rephrasing your question.")
                    st.info("💡 Tip: Try using more specific words or describing your topic in detail for better matches.")
    
    elif selected == "Explore Themes":
        st.markdown('<h1 class="main-header">📚 Explore Themes</h1>', unsafe_allow_html=True)
        
        # Search functionality
        st.subheader("🔍 Search Kurals")
        search_option = st.radio("Search by:", ["Theme", "Keyword", "Kural Number"])
        
        # Display options - moved below Search Kurals section
        st.markdown("---")
        with st.expander("⚙️ Display Options", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                show_transliteration = st.checkbox("Show Transliteration", value=True, key="theme_translit")
            with col2:
                # Get available Tamil explanations from a sample kural to determine options
                sample_kural = None
                for theme, kurals in COMPREHENSIVE_KURAL_DATABASE.items():
                    if kurals:
                        sample_kural = kurals[0]
                        break
                
                available_explanations = []
                if sample_kural:
                    if sample_kural.get('mv'):
                        available_explanations.append(("மு.வரதராசனார்", 'mv'))
                    if sample_kural.get('sp'):
                        available_explanations.append(("சாலமன் பாப்பையா", 'sp'))
                    if sample_kural.get('mk'):
                        available_explanations.append(("மு.கருணாநிதி", 'mk'))
                
                if len(available_explanations) > 1:
                    selected_explanation = st.expander(
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
        
        if search_option == "Theme":
            # Theme selection
            theme_options = list(COMPREHENSIVE_KURAL_DATABASE.keys())
            selected_theme = st.selectbox("Choose a theme to explore:", theme_options)
            
            if st.button("Search", key="theme_search"):
                if selected_theme:
                    st.subheader(f"📖 {selected_theme.title()} - Thirukkural Verses")
                    st.info(f"Found {len(COMPREHENSIVE_KURAL_DATABASE[selected_theme])} kurals in this theme")
                    
                    theme_kurals = COMPREHENSIVE_KURAL_DATABASE[selected_theme]
                    for kural in theme_kurals:
                        display_kural(kural, show_transliteration=show_transliteration, show_english=True)
                        st.markdown("<br>", unsafe_allow_html=True)
        
        elif search_option == "Keyword":
            keyword = st.text_input("Enter a keyword to search in kurals:")
            if st.button("Search", key="keyword_search"):
                if keyword:
                    with st.spinner("Searching using our enhanced RAG system..."):
                        # Use the enhanced RAG approach for better results
                        emotions = detect_emotion(keyword)
                        themes = detect_theme(keyword)
                        matching_kurals_with_details = find_relevant_kurals_rag(keyword, emotions, themes)
                        
                        if matching_kurals_with_details:
                            # Limit to 10 most relevant kurals
                            limited_kurals_with_details = matching_kurals_with_details[:10]
                            st.subheader(f"🔍 Search Results for '{keyword}'")
                            st.info(f"Found {len(matching_kurals_with_details)} matching kurals using our enhanced RAG system, showing top 10 most relevant")
                            
                            for kural, details in limited_kurals_with_details:
                                display_kural(kural, show_transliteration=show_transliteration, show_english=True)
                                
                                # Enhanced match details display
                                with st.expander(f"🔍 Why this Kural is relevant (Score: {sum(1 for d in details if 'match' in d.lower())} matches)"):
                                    for detail in details:
                                        if "Exact theme match" in detail:
                                            st.success(f"✅ {detail}")
                                        elif "Partial theme match" in detail:
                                            st.info(f"🔗 {detail}")
                                        elif "Emotion match" in detail:
                                            st.warning(f"💭 {detail}")
                                        elif "Emotional context" in detail:
                                            st.warning(f"💭 {detail}")
                                        elif "English matches" in detail:
                                            st.success(f"📝 {detail}")
                                        elif "Meaning matches" in detail:
                                            st.success(f"📖 {detail}")
                                        elif "Couplet matches" in detail:
                                            st.info(f"📜 {detail}")
                                        else:
                                            st.write(f"• {detail}")
                                
                                st.markdown("<br>", unsafe_allow_html=True)
                            
                            if len(matching_kurals_with_details) > 10:
                                st.info(f"💡 There are {len(matching_kurals_with_details) - 10} more results. Refine your search for more specific results.")
                        else:
                            st.warning(f"No kurals found matching '{keyword}'")
                            st.info("💡 Tip: Try using more specific words or describing your topic in detail for better matches.")
                else:
                    st.warning("Please enter a keyword to search")
        
        elif search_option == "Kural Number":
            kural_numbers_input = st.text_input("Enter Kural numbers separated by comma (e.g., 1, 2, 3):", placeholder="1, 2, 3")
            
            if st.button("Search", key="number_search"):
                if kural_numbers_input.strip():
                    # Parse comma-separated numbers
                    try:
                        kural_numbers = [int(num.strip()) for num in kural_numbers_input.split(',') if num.strip().isdigit()]
                        kural_numbers = [num for num in kural_numbers if 1 <= num <= 1330]  # Validate range
                        
                        if kural_numbers:
                            st.subheader(f"📖 Kurals #{', '.join(map(str, kural_numbers))}")
                            found_kurals = []
                            
                            for kural_num in kural_numbers:
                                kural = get_kural_by_number(kural_num)
                                if kural:
                                    found_kurals.append(kural)
                                else:
                                    st.warning(f"Kural #{kural_num} not found in the current database")
                            
                            if found_kurals:
                                st.info(f"Found {len(found_kurals)} out of {len(kural_numbers)} requested kurals")
                                for kural in found_kurals:
                                    display_kural(kural, show_transliteration=show_transliteration, show_english=True)
                                    st.markdown("<br>", unsafe_allow_html=True)
                        else:
                            st.warning("Please enter valid Kural numbers between 1 and 1330")
                    except ValueError:
                        st.error("Please enter valid numbers separated by commas")
                else:
                    st.warning("Please enter Kural numbers to search")
        

    
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
        
        **Enhanced RAG-Powered AI Mode**
        - Interactive dialogue with ancient wisdom using advanced retrieval
        - Personalized guidance based on multi-dimensional analysis
        - Intelligent matching across emotions, themes, and content
        - Detailed explanations of why each verse is relevant
        
        ### 📖 About Thirukkural
        
        Thirukkural is a classic Tamil text consisting of 1,330 couplets dealing with the everyday virtues of an individual. 
        It is one of the most important works in Tamil literature and is considered a masterpiece of ethical literature.
        
        The text is divided into three sections:
        - **Aram (Virtue)** - 380 verses on moral values
        - **Porul (Wealth)** - 700 verses on political and economic matters  
        - **Inbam (Love)** - 250 verses on human love and relationships
        
        ### 🚀 Technology
        
        Built with Streamlit, Python, and AI-powered emotion detection to bridge ancient wisdom with modern technology.
        
        **Enhanced RAG (Retrieval-Augmented Generation) System:**
        - Multi-dimensional search across English, meaning, theme, and couplet fields
        - Intelligent scoring based on emotional alignment, thematic relevance, and content matching
        - Contextual understanding of user queries for better verse selection
        - Detailed explanations of why each verse is relevant to the user's situation
        
        ### 📁 Database Structure
        
        The Kural database is organized into multiple files for better maintainability:
        - `kural_database.py` - Main database with core kurals
        - `comprehensive_kurals.py` - Additional kurals for extended coverage
        - `extended_kurals.py` - Further kurals for maximum coverage
        
        This modular approach allows for easy expansion and maintenance of the database.
        """)

if __name__ == "__main__":
    main()