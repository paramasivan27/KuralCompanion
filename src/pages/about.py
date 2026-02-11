"""About page."""

import streamlit as st
import pandas as pd
import plotly.express as px

from aggregated_kurals import get_aggregated_chapters
from kural_logic import get_theme_counts, get_total_kural_count


def render_about():
    st.markdown(
        '<h1 class="main-header">ℹ️ About KuralCompanion</h1>',
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(
            "Thiruvalluvar_Final.png",
            use_container_width=True,
            caption="Thiruvalluvar - The Great Sage",
        )
    st.markdown('<hr class="hr-kolam">', unsafe_allow_html=True)

    total_kurals = get_total_kural_count()
    theme_counts = get_theme_counts()
    total_chapters = len(get_aggregated_chapters())

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total Kurals in Database", total_kurals)
        st.metric("Themes Covered", len(theme_counts))
    with c2:
        st.metric("Target Goal", "1,330 Kurals")
        st.metric("Coverage", f"{(total_kurals / 1330) * 100:.1f}%")
    with c3:
        st.metric("Aggregated Chapters", total_chapters)
        st.metric("Enhanced RAG", "✓ Active")

    st.subheader("📊 Database Coverage by Theme")
    theme_data = pd.DataFrame(
        list(theme_counts.items()), columns=["Theme", "Count"]
    )
    fig = px.bar(theme_data, x="Theme", y="Count", title="Kurals per Theme")
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

    ### 🔍 How KuralCompanion Works

    **Enhanced RAG (Retrieval-Augmented Guidance)**
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
