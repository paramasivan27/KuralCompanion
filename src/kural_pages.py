"""All page renderers in a non-reserved module name.

Using a module (not a `pages/` directory) avoids Streamlit auto multipage
sidebar injection, which conflicted with the custom sidebar menu.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from aggregated_kurals import get_aggregated_chapters
from app_state import COMPREHENSIVE_KURAL_DATABASE, get_kural_by_number_comprehensive
from kural_logic import (
    detect_theme,
    find_relevant_kurals_rag,
    generate_contextual_response,
    generate_llm_summary,
    llm_available,
    get_theme_counts,
    get_total_kural_count,
)
from ui_components import (
    display_kural,
    render_match_details_expander,
    render_display_options_expander,
)


def render_home():
    st.markdown('<h1 class="main-header">🌟 KuralCompanion</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Ancient Wisdom for Modern Life</p>', unsafe_allow_html=True)

    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            """
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
        """
        )
        st.image(
            "Thiruvalluvar_Small.png",
            use_container_width=True,
            caption="Thiruvalluvar - The Great Sage",
        )
        st.markdown('<hr class="hr-kolam">', unsafe_allow_html=True)
        if st.button("🚀 Start Your Journey", type="primary"):
            st.session_state.selected_page = "Ask Kural"
            st.rerun()


def render_ask_kural():
    st.markdown('<h1 class="main-header">💡 Ask Kural</h1>', unsafe_allow_html=True)

    user_input = st.text_area(
        "Ask about any topic, concept, or subject...",
        placeholder="e.g., 'Tell me about Rain' or 'Tell me about Friendship' or 'What does Thirukkural say about Leadership?'",
        height=100,
        key="ask_kural_user_input",
    )

    st.markdown("---")
    show_transliteration = render_display_options_expander("ask_kural")

    if st.button("💡 Know Thirukkural", type="primary") and user_input:
        with st.spinner("Searching for relevant wisdom using our enhanced RAG system..."):
            themes = detect_theme(user_input)
            relevant_kurals_with_details = find_relevant_kurals_rag(user_input, themes)

            if relevant_kurals_with_details:
                st.markdown("---")
                st.subheader("🤖 KuralCompanion's Response")
                contextual_response = generate_contextual_response(
                    user_input, themes, relevant_kurals_with_details
                )
                st.markdown(
                    f"""
                **Your Question:** "{user_input}"

                **KuralCompanion's Response:** {contextual_response}
                """
                )
                st.markdown("---")
                st.subheader("📖 Relevant Thirukkural Verses")
                st.info(
                    f"Found {len(relevant_kurals_with_details)} highly relevant kurals "
                    "using our enhanced RAG system"
                )
                for i, (kural, details) in enumerate(relevant_kurals_with_details):
                    display_kural(
                        kural,
                        i,
                        show_transliteration=show_transliteration,
                        show_english=True,
                    )
                    render_match_details_expander(details)

                if llm_available():
                    st.markdown("---")
                    if st.button("✨ Summarize with AI", key="llm_summarize"):
                        kurals_tuple = tuple(
                            (k.get("english", ""), k.get("meaning", ""), k.get("number", ""))
                            for k, _ in relevant_kurals_with_details
                        )
                        with st.spinner("Generating AI synthesis..."):
                            summary = generate_llm_summary(user_input, kurals_tuple)
                        if summary:
                            st.markdown("### 🤖 AI Synthesis")
                            st.info(summary)
                        else:
                            st.warning("AI summary unavailable. Please try again.")
            else:
                st.warning(
                    "No relevant Kurals found for your query. "
                    "Try using different keywords or rephrasing your question."
                )
                st.info(
                    "💡 Tip: Try using more specific words or describing your topic in detail for better matches."
                )


def render_explore_themes():
    st.markdown('<h1 class="main-header">📚 Explore Themes</h1>', unsafe_allow_html=True)
    st.subheader("🔍 Search Kurals")
    search_option = st.radio("Search by:", ["Theme", "Keyword", "Kural Number"])

    st.markdown("---")
    show_transliteration = render_display_options_expander("theme")

    if search_option == "Theme":
        theme_options = list(COMPREHENSIVE_KURAL_DATABASE.keys())
        selected_theme = st.selectbox("Choose a theme to explore:", theme_options)
        if st.button("Search", key="theme_search") and selected_theme:
            st.subheader(f"📖 {selected_theme.title()} - Thirukkural Verses")
            theme_kurals = COMPREHENSIVE_KURAL_DATABASE[selected_theme]
            st.info(f"Found {len(theme_kurals)} kurals in this theme")
            for kural in theme_kurals:
                display_kural(
                    kural, show_transliteration=show_transliteration, show_english=True
                )
                st.markdown("<br>", unsafe_allow_html=True)

    elif search_option == "Keyword":
        keyword = st.text_input(
            "Enter a keyword to search in kurals:", key="theme_keyword_search"
        )
        if st.button("Search", key="keyword_search"):
            if not keyword:
                st.warning("Please enter a keyword to search")
            else:
                with st.spinner("Searching using our enhanced RAG system..."):
                    themes = detect_theme(keyword)
                    matching = find_relevant_kurals_rag(keyword, themes)
                    if matching:
                        limited = matching[:10]
                        st.subheader(f"🔍 Search Results for '{keyword}'")
                        st.info(
                            f"Found {len(matching)} matching kurals, showing top 10 most relevant"
                        )
                        for kural, details in limited:
                            display_kural(
                                kural,
                                show_transliteration=show_transliteration,
                                show_english=True,
                            )
                            render_match_details_expander(details)
                            st.markdown("<br>", unsafe_allow_html=True)
                        if len(matching) > 10:
                            st.info(
                                f"💡 There are {len(matching) - 10} more results. "
                                "Refine your search for more specific results."
                            )
                    else:
                        st.warning(f"No kurals found matching '{keyword}'")
                        st.info(
                            "💡 Tip: Try using more specific words or describing your topic in detail."
                        )

    elif search_option == "Kural Number":
        kural_numbers_input = st.text_input(
            "Enter Kural numbers separated by comma (e.g., 1, 2, 3):",
            placeholder="1, 2, 3",
            key="theme_number_search",
        )
        if st.button("Search", key="number_search") and kural_numbers_input.strip():
            try:
                kural_numbers = [
                    int(num.strip())
                    for num in kural_numbers_input.split(",")
                    if num.strip().isdigit()
                ]
                kural_numbers = [n for n in kural_numbers if 1 <= n <= 1330]
                if kural_numbers:
                    st.subheader(f"📖 Kurals #{', '.join(map(str, kural_numbers))}")
                    found = []
                    for num in kural_numbers:
                        kural = get_kural_by_number_comprehensive(num)
                        if kural:
                            found.append(kural)
                        else:
                            st.warning(f"Kural #{num} not found in the current database")
                    if found:
                        st.info(
                            f"Found {len(found)} out of {len(kural_numbers)} requested kurals"
                        )
                        for kural in found:
                            display_kural(
                                kural,
                                show_transliteration=show_transliteration,
                                show_english=True,
                            )
                            st.markdown("<br>", unsafe_allow_html=True)
                else:
                    st.warning("Please enter valid Kural numbers between 1 and 1330")
            except ValueError:
                st.error("Please enter valid numbers separated by commas")
        elif st.button("Search", key="number_search"):
            st.warning("Please enter Kural numbers to search")


def render_browse_summaries():
    st.markdown(
        '<h1 class="main-header">📚 Browse Chapter Summaries</h1>',
        unsafe_allow_html=True,
    )
    st.info(
        "Explore all available themes and their wisdom summaries from the aggregated Thirukkural database"
    )

    all_chapters = get_aggregated_chapters()
    if not all_chapters:
        st.warning("No chapters available in the aggregated database")
        return

    chapter_search = st.text_input(
        "🔍 Search chapters by name or content:",
        placeholder="e.g., 'rain', 'friendship', 'leadership'",
    )
    if chapter_search:
        search_lower = chapter_search.lower()
        display_chapters = [
            ch
            for ch in all_chapters
            if search_lower in ch["Chapter"].lower()
            or any(search_lower in point.lower() for point in ch.get("Summary", []))
        ]
    else:
        display_chapters = all_chapters

    cols = st.columns(3)
    for i, chapter in enumerate(display_chapters):
        col_idx = i % 3
        with cols[col_idx]:
            with st.expander(f"🎯 {chapter['Chapter']}", expanded=False):
                st.markdown(f"**{chapter['Chapter']}**")
                st.markdown(f"*{len(chapter.get('Kurals', []))} kurals*")
                if chapter.get("Summary"):
                    st.markdown("**Key Insights:**")
                    for point in chapter["Summary"][:2]:
                        st.markdown(f"• {point}")
                if chapter.get("Kurals"):
                    sample = chapter["Kurals"][0]
                    st.markdown("**Sample Kural:**")
                    st.markdown(
                        f"**#{sample.get('Number', 'Unknown')}:** "
                        f"{sample.get('Translation', 'No translation')[:100]}..."
                    )
                if st.button(f"View Details", key=f"browse_{i}"):
                    st.session_state[f"browse_expanded_{i}"] = not st.session_state.get(
                        f"browse_expanded_{i}", False
                    )
                    st.rerun()

                if st.session_state.get(f"browse_expanded_{i}", False):
                    st.markdown("---")
                    st.markdown("**📝 Full Chapter Summary:**")
                    if chapter.get("Summary"):
                        for j, point in enumerate(chapter["Summary"], 1):
                            st.markdown(f"{j}. {point}")
                    st.markdown("**📚 All Kurals in this Chapter:**")
                    if chapter.get("Kurals"):
                        for _, kural in enumerate(chapter["Kurals"][:5]):
                            with st.expander(
                                f"Kural #{kural.get('Number', 'Unknown')} - "
                                f"{kural.get('Translation', 'No translation')[:50]}...",
                                expanded=False,
                            ):
                                st.markdown(
                                    f"**Kural #{kural.get('Number', 'Unknown')}**"
                                )
                                if kural.get("Translation"):
                                    st.markdown(
                                        f"**Translation:** {kural['Translation']}"
                                    )
                                if kural.get("Explanation"):
                                    st.markdown(
                                        f"**Explanation:** {kural['Explanation']}"
                                    )
                                if kural.get("Couplet"):
                                    st.markdown(f"**Couplet:** {kural['Couplet']}")
                        if len(chapter["Kurals"]) > 5:
                            st.info(
                                f"... and {len(chapter['Kurals']) - 5} more kurals"
                            )

    if chapter_search and not display_chapters:
        st.warning(f"No chapters found matching '{chapter_search}'")
        st.info("💡 Try different keywords or browse all chapters above")


def render_about():
    st.markdown(
        '<h1 class="main-header">ℹ️ About KuralCompanion</h1>',
        unsafe_allow_html=True,
    )
    _, col2, _ = st.columns([1, 2, 1])
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
    theme_data = pd.DataFrame(list(theme_counts.items()), columns=["Theme", "Count"])
    fig = px.bar(theme_data, x="Theme", y="Count", title="Kurals per Theme")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
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
    """
    )
