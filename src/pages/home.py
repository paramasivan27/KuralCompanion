"""Home page."""

import streamlit as st


def render_home():
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
        st.image("Thiruvalluvar_Small.png", use_container_width=True, caption="Thiruvalluvar - The Great Sage")
        st.markdown('<hr class="hr-kolam">', unsafe_allow_html=True)
        if st.button("🚀 Start Your Journey", type="primary"):
            st.session_state.selected_page = "Ask Kural"
            st.rerun()
