import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import re
from collections import defaultdict
import json
from streamlit_option_menu import option_menu
# Direct imports for Hugging Face Space deployment
from kural_database import KURAL_DATABASE, THEME_KEYWORDS, get_all_kurals, get_kural_by_number, get_kurals_by_theme, search_kurals_by_keyword
from comprehensive_kurals import KURAL_DATABASE as COMPREHENSIVE_KURALS
from extended_kurals import KURAL_DATABASE as EXTENDED_KURALS
from aggregated_kurals import AGGREGATED_KURALS_DATA, get_aggregated_chapters

# Create comprehensive database by merging all three databases for maximum coverage
def merge_all_kural_databases(core_db, comprehensive_db, extended_db):
    """Merge all three kural databases into one comprehensive database"""
    merged_db = {}
    
    # Merge core database
    for theme, kurals in core_db.items():
        merged_db[theme] = kurals
    
    # Merge comprehensive database
    for theme, kurals in comprehensive_db.items():
        if theme in merged_db:
            merged_db[theme].extend(kurals)
        else:
            merged_db[theme] = kurals
    
    # Merge extended database
    for theme, kurals in extended_db.items():
        if theme in merged_db:
            merged_db[theme].extend(kurals)
        else:
            merged_db[theme] = kurals
    
    return merged_db

COMPREHENSIVE_KURAL_DATABASE = merge_all_kural_databases(KURAL_DATABASE, COMPREHENSIVE_KURALS, EXTENDED_KURALS)

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
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700&family=Noto+Sans+Tamil:wght@300;400;500;600;700&family=Noto+Serif+Tamil:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap');
    
    /* CSS Custom Properties for Palm Leaf Theme */
    :root {
        /* Classic Palm-Leaf Theme */
        --palm-leaf: #DAC7A0;
        --temple-stone: #2B2A28;
        --kumkum-red: #A2322E;
        --turmeric-gold: #D3A014;
        --indigo-ink: #1F3C88;
        --soft-sand: #F5EEDC;
        
        /* Theme variables */
        --primary: var(--palm-leaf);
        --secondary: var(--temple-stone);
        --accent: var(--kumkum-red);
        --accent-secondary: var(--turmeric-gold);
        --link: var(--indigo-ink);
        --surface: var(--soft-sand);
        --text: var(--temple-stone);
        --text-light: #666;
        --background: #ffffff;
    }
    }
    
    /* Global Styles */
    .stApp {
        background: var(--background) !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif;
    }
    

    

    

    

    
    /* Typography */
    .main-header {
        font-family: 'EB Garamond', serif;
        font-size: 3.5rem;
        font-weight: 600;
        text-align: center;
        color: var(--primary) !important;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        position: relative;
        transition: color 0.3s ease;
    }
    

    
    .sub-header {
        font-family: 'Noto Serif Tamil', serif;
        font-size: 1.8rem;
        text-align: center;
        color: var(--text-light);
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Kural Card with enhanced design */
    .kural-card {
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        border: 2px solid var(--accent-secondary);
        position: relative;
        overflow: hidden;
    }
    
    .kural-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="palm" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M10 0L12 8L20 10L12 12L10 20L8 12L0 10L8 8Z" fill="white" opacity="0.05"/></pattern></defs><rect width="100" height="100" fill="url(%23palm)"/></svg>');
        opacity: 0.1;
    }
    
    /* Kolam divider */
    .hr-kolam {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, var(--accent) 50%, transparent 100%);
        border: none;
        margin: 2rem 0;
        position: relative;
    }
    
    .hr-kolam::before {
        content: '•';
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        color: var(--accent);
        font-size: 1.5rem;
        background: var(--background);
        padding: 0 1rem;
    }
    
    /* Theme Badges */
    .theme-badge {
        display: inline-block;
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        font-weight: 600;
        margin: 0.3rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
        background: linear-gradient(135deg, #6c5ce7, #5f3dc4);
        color: white;
    }
    
    .theme-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    /* Tamil Text Styling */
    .tamil-text {
        font-family: 'Noto Serif Tamil', serif;
        font-size: 1.2rem;
        line-height: 1.8;
        color: var(--text);
    }
    
    /* Section Headers with Motifs */
    .section-header {
        font-family: 'EB Garamond', serif;
        font-size: 2.5rem;
        color: var(--primary);
        margin: 2rem 0 1rem 0;
        position: relative;
        padding-left: 3rem;
    }
    
    .section-header::before {
        content: '🎵'; /* Yazh (ancient lute) emoji as placeholder */
        position: absolute;
        left: 0;
        top: 0;
        font-size: 2rem;
        opacity: 0.7;
    }
    
    /* Enhanced Form Elements */
    .stTextInput > div > div > input {
        border: 2px solid var(--accent);
        border-radius: 15px;
        padding: 12px 16px;
        font-family: 'Inter', sans-serif;
        background: var(--surface);
        color: var(--text);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--accent-secondary);
        box-shadow: 0 0 0 3px rgba(211, 160, 20, 0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, var(--accent), var(--accent-secondary));
        color: white;
        border: none;
        border-radius: 15px;
        padding: 12px 24px;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: var(--surface);
        border-right: 2px solid var(--accent);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        
        .sub-header {
            font-size: 1.4rem;
        }
        
        .kural-card {
            padding: 1.5rem;
        }
        

    }
    
    /* Additional Utility Classes */
    .tamil-quote {
        font-family: 'Noto Serif Tamil', serif;
        font-size: 1.4rem;
        line-height: 2;
        color: var(--primary);
        text-align: center;
        margin: 2rem 0;
        padding: 2rem;
        background: var(--surface);
        border-radius: 15px;
        border-left: 4px solid var(--accent);
    }
    
    .kural-number {
        font-family: 'EB Garamond', serif;
        font-size: 1.2rem;
        color: var(--accent-secondary);
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .explanation-text {
        font-family: 'Inter', sans-serif;
        line-height: 1.7;
        color: var(--text);
        margin: 1rem 0;
    }
    
    /* Enhanced sidebar styling */
    .css-1d391kg .css-1lcbmhc {
        background: var(--surface);
        border-right: 2px solid var(--accent);
    }
    
    /* Streamlit specific overrides */
    .stMarkdown {
        color: var(--text);
    }
    
    .stText {
        color: var(--text);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--surface);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--accent);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-secondary);
    }
</style>


""", unsafe_allow_html=True)

# Thirukkural Database is now imported from kural_database.py

# Theme keywords are now imported from kural_database.py


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

def find_relevant_kurals_rag(user_input, themes):
    """Find relevant Kurals using enhanced RAG approach - searching across multiple fields for better relevance"""
    # Normalize inputs
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
                    match_details.append(term)
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
    # Create a mock user input and detect themes
    mock_input = " ".join(search_keywords)
    themes = detect_theme(mock_input)
    
    # Use the enhanced RAG function
    relevant_kurals_with_details = find_relevant_kurals_rag(mock_input, themes)
    
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
            explanations_html += f"<p><em>மு.வரதராசனார்:</em><br><span class='tamil-text'>{mv}</span></p>"
        elif selected_key == 'sp' and sp:
            explanations_html += f"<p><em>சாலமன் பாப்பையா:</em><br><span class='tamil-text'>{sp}</span></p>"
        elif selected_key == 'mk' and mk:
            explanations_html += f"<p><em>மு.கருணாநிதி:</em><br><span class='tamil-text'>{mk}</span></p>"
        else:
            # Fallback: show first available explanation
            if mv:
                explanations_html += f"<p><em>மு.வரதராசனார்:</em><br><span class='tamil-text'>{mv}</span></p>"
            elif sp:
                explanations_html += f"<p><em>சாலமன் பாப்பையா:</em><br><span class='tamil-text'>{sp}</span></p>"
            elif mk:
                explanations_html += f"<p><em>மு.கருணாநிதி:</em><br><span class='tamil-text'>{mk}</span></p>"
    
    # Build conditional sections
    sections_html = [
        f"<p><strong>Tamil:</strong><br><span class='tamil-text'>{tamil_text}</span></p>"
    ]
    if show_translit and transliteration_text:
        sections_html.append(f"<p><strong>Transliteration:</strong><br>{transliteration_text}</p>")
    if show_english:
        sections_html.append(f"<p><strong>English:</strong> {kural['english']}</p>")
    sections_html.append(f"<p><strong>Meaning:</strong> {kural['meaning']}</p>")
    if explanations_html:
        sections_html.append(explanations_html)


    st.markdown(
        f"""
        <div class="kural-card">
            <div class="kural-number">Kural #{kural['number']}</div>
            {''.join(sections_html)}
        </div>
        """,
        unsafe_allow_html=True,
    )


def generate_contextual_response(user_input, themes, kurals_with_details):
    """Generate an enhanced contextual response based on user input, themes, and found kurals using RAG insights"""
    response_parts = []
    
    # Start with contextual acknowledgment
    response_parts.append("Thirukkural's timeless wisdom offers profound guidance for your question. Let me share the most relevant verses that directly address your inquiry.")
    
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
            response_parts.append(f"I've found Kural #{kural_numbers[0]}, which directly addresses your question with remarkable precision.")
        else:
            response_parts.append(f"I've found {len(kural_numbers)} highly relevant kurals (#{', '.join(map(str, kural_numbers))}) that directly address your question.")
        
        # Add insights about why these kurals are relevant
        response_parts.append("These verses were selected because they address your themes and contain content that directly relates to your question.")
        
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
    
    # Add general guidance
    response_parts.append("Thirukkural's wisdom is timeless because it addresses the fundamental aspects of human experience that remain constant across generations.")
    
    return ' '.join(response_parts)



def clear_page_state():
    """Clear all page-related state variables to ensure clean navigation"""
    keys_to_clear = [
        'user_input', 'search_results', 'theme_analysis',
        'show_transliteration', 'selected_explanation'
    ]
    
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

# Main app
def main():
    # Initialize session state for navigation
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "Home"
    
    # Clear any previous page content to prevent bleeding
    st.empty()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## 🌟 KuralCompanion")
        sidebar_selected = option_menu(
            menu_title=None,
            options=["Home", "Ask Kural", "Explore Themes", "Browse Chapter Summaries", "About"],
            icons=["house", "lightbulb", "book", "book-open", "info-circle"],
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
        
        # Clear all page state and force a complete refresh
        clear_page_state()
        
        # Force a complete page refresh to clear all displayed content
        st.rerun()
    
    selected = st.session_state.selected_page
    
    # Create a container for the main content to ensure proper isolation
    main_container = st.container()
    
    with main_container:
        if selected == "Home":
            st.markdown('<h1 class="main-header">🌟 KuralCompanion</h1>', unsafe_allow_html=True)
            st.markdown('<p class="sub-header">Ancient Wisdom for Modern Life</p>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                st.markdown("""
                ### Welcome to Your Digital Sage
                
                KuralCompanion is your guide to the timeless wisdom of Thiruvalluvar's Thirukkural. 
                Whether you're seeking advice, exploring themes, or asking life's deeper questions, 
                let the ancient verses illuminate your path.
                
                **How it works:**
                - Share your thoughts, feelings, or questions
                - Our enhanced RAG system analyzes your input across multiple dimensions
                - AI detects themes and contextual relevance
                - Receive highly relevant Thirukkural verses with detailed explanations
                - Understand why each verse was selected for your situation
                
                Start your journey by asking a question or sharing how you feel!
                """)
                
                # Display Thiruvalluvar image
                st.image("Thiruvalluvar_Small.png", use_container_width=True, caption="Thiruvalluvar - The Great Sage")
                
                # Kolam divider
                st.markdown('<hr class="hr-kolam">', unsafe_allow_html=True)
                
                if st.button("🚀 Start Your Journey", type="primary"):
                    st.session_state.selected_page = "Ask Kural"
                    st.rerun()
        
        
        elif selected == "Ask Kural":
            st.markdown('<h1 class="main-header">💡 Ask Kural</h1>', unsafe_allow_html=True)
            
            # User input
            user_input = st.text_area(
                "Ask about any topic, concept, or subject...",
                placeholder="e.g., 'Tell me about Rain' or 'Tell me about Friendship' or 'What does Thirukkural say about Leadership?'",
                height=100,
                key="ask_kural_user_input"
                )
            
            # Display options - similar to Ask Kural section
            st.markdown("---")
            with st.expander("⚙️ Display Options", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    show_transliteration = st.checkbox("Show Transliteration", value=True, key="ask_kural_translit")
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
                            key="ask_kural_explanation"
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
                    # Detect themes for better context
                    themes = detect_theme(user_input)
                    
                    # Use the enhanced RAG approach for better results
                    relevant_kurals_with_details = find_relevant_kurals_rag(user_input, themes)
                    

                    
                    if relevant_kurals_with_details:
                        st.markdown("---")
                        st.subheader("🤖 KuralCompanion's Response")
                        
                        # Generate contextual response
                        contextual_response = generate_contextual_response(user_input, themes, relevant_kurals_with_details)
                        
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
                keyword = st.text_input("Enter a keyword to search in kurals:", key="theme_keyword_search")
                if st.button("Search", key="keyword_search"):
                    if keyword:
                        with st.spinner("Searching using our enhanced RAG system..."):
                            # Use the enhanced RAG approach for better results
                            themes = detect_theme(keyword)
                            matching_kurals_with_details = find_relevant_kurals_rag(keyword, themes)
                            

                            
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
                kural_numbers_input = st.text_input("Enter Kural numbers separated by comma (e.g., 1, 2, 3):", placeholder="1, 2, 3", key="theme_number_search")
                
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
        
        
        
        elif selected == "Browse Chapter Summaries":
            st.markdown('<h1 class="main-header">📚 Browse Chapter Summaries</h1>', unsafe_allow_html=True)
            st.info("Explore all available themes and their wisdom summaries from the aggregated Thirukkural database")
            
            # Get all chapters from aggregated data
            all_chapters = get_aggregated_chapters()
            
            if all_chapters:
                # Create a search filter for chapters
                chapter_search = st.text_input("🔍 Search chapters by name or content:", placeholder="e.g., 'rain', 'friendship', 'leadership'")
                
                # Filter chapters based on search
                if chapter_search:
                    filtered_chapters = []
                    search_lower = chapter_search.lower()
                    for chapter in all_chapters:
                        if (search_lower in chapter["Chapter"].lower() or
                            any(search_lower in point.lower() for point in chapter.get("Summary", []))):
                            filtered_chapters.append(chapter)
                    display_chapters = filtered_chapters
                else:
                    display_chapters = all_chapters
                
                # Display chapters in a grid layout
                cols = st.columns(3)
                for i, chapter in enumerate(display_chapters):
                    col_idx = i % 3
                    with cols[col_idx]:
                        with st.expander(f"🎯 {chapter['Chapter']}", expanded=False):
                            st.markdown(f"**{chapter['Chapter']}**")
                            st.markdown(f"*{len(chapter.get('Kurals', []))} kurals*")
                            
                            if chapter.get("Summary"):
                                st.markdown("**Key Insights:**")
                                for point in chapter["Summary"][:2]:  # Show first 2 summary points
                                    st.markdown(f"• {point}")
                            
                            # Show a sample kural
                            if chapter.get("Kurals"):
                                sample_kural = chapter["Kurals"][0]
                                st.markdown("**Sample Kural:**")
                                st.markdown(f"**#{sample_kural.get('Number', 'Unknown')}:** {sample_kural.get('Translation', 'No translation')[:100]}...")
                            
                            if st.button(f"View Details", key=f"browse_{i}"):
                                # Toggle the expander to show more details
                                st.session_state[f"browse_expanded_{i}"] = not st.session_state.get(f"browse_expanded_{i}", False)
                                st.rerun()
                            
                            # Show expanded details if button was clicked
                            if st.session_state.get(f"browse_expanded_{i}", False):
                                st.markdown("---")
                                st.markdown("**📝 Full Chapter Summary:**")
                                if chapter.get("Summary"):
                                    for j, point in enumerate(chapter["Summary"], 1):
                                        st.markdown(f"{j}. {point}")
                                
                                st.markdown("**📚 All Kurals in this Chapter:**")
                                if chapter.get("Kurals"):
                                    for k, kural in enumerate(chapter["Kurals"][:5]):  # Show first 5 kurals
                                        with st.expander(f"Kural #{kural.get('Number', 'Unknown')} - {kural.get('Translation', 'No translation')[:50]}...", expanded=False):
                                            st.markdown(f"**Kural #{kural.get('Number', 'Unknown')}**")
                                            if kural.get('Translation'):
                                                st.markdown(f"**Translation:** {kural['Translation']}")
                                            if kural.get('Explanation'):
                                                st.markdown(f"**Explanation:** {kural['Explanation']}")
                                            if kural.get('Couplet'):
                                                st.markdown(f"**Couplet:** {kural['Couplet']}")
                                    if len(chapter["Kurals"]) > 5:
                                        st.info(f"... and {len(chapter['Kurals']) - 5} more kurals")
                
                if chapter_search and not filtered_chapters:
                    st.warning(f"No chapters found matching '{chapter_search}'")
                    st.info("💡 Try different keywords or browse all chapters above")
            else:
                st.warning("No chapters available in the aggregated database")
        
        elif selected == "About":
            st.markdown('<h1 class="main-header">ℹ️ About KuralCompanion</h1>', unsafe_allow_html=True)
            
            # Display Thiruvalluvar image
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image("Thiruvalluvar_Final.png", use_container_width=True, caption="Thiruvalluvar - The Great Sage")
            
            # Kolam divider
            st.markdown('<hr class="hr-kolam">', unsafe_allow_html=True)
            
            # Database Statistics
            total_kurals = get_total_kural_count()
            theme_counts = get_theme_counts()
            total_chapters = len(get_aggregated_chapters())
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Kurals in Database", total_kurals)
                st.metric("Themes Covered", len(theme_counts))
            
            with col2:
                st.metric("Target Goal", "1,330 Kurals")
                st.metric("Coverage", f"{(total_kurals/1330)*100:.1f}%")
            
            with col3:
                st.metric("Aggregated Chapters", total_chapters)
                st.metric("Enhanced RAG", "✓ Active")
            
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
            - Organized by themes for intelligent matching
            - Multiple database files for better organization and scalability
            - **NEW: Aggregated data with chapter-level summaries for enhanced wisdom insights**
            
            **Theme-Based Kural Discovery**
            - Detects themes from your input for intelligent matching
            - Maps to relevant Thirukkural verses
            - Provides contextual meanings and reflections
            
            **Enhanced RAG-Powered AI Mode**
            - Interactive dialogue with ancient wisdom using advanced retrieval
            - Personalized guidance based on multi-dimensional analysis
            - Intelligent matching across themes and content
            - Detailed explanations of why each verse is relevant
            
            ### 📖 About Thirukkural
            
            Thirukkural is a classic Tamil text consisting of 1,330 couplets dealing with the everyday virtues of an individual. 
            It is one of the most important works in Tamil literature and is considered a masterpiece of ethical literature.
            
            The text is divided into three sections:
            - **Aram (Virtue)** - 380 verses on moral values
            - **Porul (Wealth)** - 700 verses on political and economic matters  
            - **Inbam (Love)** - 250 verses on human love and relationships
            
            ### 🚀 Technology
            
            Built with Streamlit, Python, and AI-powered theme detection to bridge ancient wisdom with modern technology.
            
            **Enhanced RAG (Retrieval-Augmented Generation) System:**
            - Multi-dimensional search across English, meaning, theme, and couplet fields
            - Intelligent scoring based on thematic relevance and content matching
            - Contextual understanding of user queries for better verse selection
            - Detailed explanations of why each verse is relevant to the user's situation
            - **NEW: Chapter-level summaries integration for deeper thematic insights and wisdom context**
            
            ### 📁 Database Structure
            
            The Kural database is organized into multiple files for better maintainability:
            - `kural_database.py` - Main database with core kurals
            - `comprehensive_kurals.py` - Additional kurals for extended coverage
            - `extended_kurals.py` - Further kurals for maximum coverage
            - **NEW: `aggregated_thirukkural_with_summary.json` - Chapter-level data with wisdom summaries**
            
            This modular approach allows for easy expansion and maintenance of the database, with the new aggregated data providing enhanced thematic insights.
            """)
        
        # Ensure no content appears outside of the selected page
        else:
            st.error("Page not found. Please select a valid page from the sidebar.")

if __name__ == "__main__":
    main()