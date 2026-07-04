"""All page renderers in a non-reserved module name.

Using a module (not a `pages/` directory) avoids Streamlit auto multipage
sidebar injection, which conflicted with the custom sidebar menu.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from aggregated_kurals import get_aggregated_chapters
from kural_database import KURAL_DATABASE as COMPREHENSIVE_KURAL_DATABASE, get_kural_by_number as get_kural_by_number_comprehensive
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

        Written over two thousand years ago, Thiruvalluvar's Thirukkural distils the whole
        of human experience into 1,330 couplets — on virtue, wealth, love, leadership,
        friendship, and the quiet dignity of everyday life. KuralCompanion brings these
        verses to you, matched to whatever is on your mind.

        ---

        **💡 Ask Kural**
        Type a question, a feeling, or a topic — *"What does Thirukkural say about patience?"*
        or simply *"I feel lost."* The app finds the most relevant verses and explains why
        each one was chosen. Optionally, let Claude AI weave them into a single insight.

        **🔍 Explore Themes**
        Browse by theme, search by keyword, or jump directly to a verse by number.
        All 1,330 kurals are indexed and searchable.

        **📖 Browse Chapters**
        Navigate all 133 chapters organised into the three great books —
        Virtue, Wealth, and Love. Each chapter includes a summary and the full
        verses in Tamil, transliteration, and English.

        ---

        *Start your journey by asking a question or sharing how you feel.*
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

    btn_col, chk_col = st.columns([2, 3])
    with btn_col:
        search_clicked = st.button("💡 Know Thirukkural", type="primary")
    with chk_col:
        include_ai = llm_available() and st.checkbox(
            "✨ Include AI Summary", value=False, key="ask_kural_include_ai"
        )

    if search_clicked and user_input:
        with st.spinner("Searching for relevant wisdom using our enhanced RAG system..."):
            themes = detect_theme(user_input)
            relevant_kurals_with_details = find_relevant_kurals_rag(user_input, themes)
        st.session_state["ask_kural_results"] = relevant_kurals_with_details
        st.session_state["ask_kural_query"] = user_input
        st.session_state["ask_kural_themes"] = themes

        if include_ai and relevant_kurals_with_details:
            kurals_tuple = tuple(
                (k.get("english", ""), k.get("meaning", ""), k.get("number", ""))
                for k, _ in relevant_kurals_with_details
            )
            with st.spinner("Generating AI synthesis..."):
                st.session_state["ask_kural_llm_summary"] = generate_llm_summary(
                    user_input, kurals_tuple
                )
        else:
            st.session_state["ask_kural_llm_summary"] = None

    results = st.session_state.get("ask_kural_results")
    query = st.session_state.get("ask_kural_query", "")
    themes = st.session_state.get("ask_kural_themes", [])
    llm_summary = st.session_state.get("ask_kural_llm_summary")

    if results is not None:
        if results:
            st.markdown("---")
            if llm_summary:
                st.subheader("🤖 KuralCompanion's AI Summary")
            else:
                st.subheader("🤖 KuralCompanion's Response")
            response_text = llm_summary if llm_summary else generate_contextual_response(
                query, themes, results
            )
            st.markdown(f'**Your Question:** "{query}"')
            st.markdown(f"**KuralCompanion's Response:** {response_text}")
            st.markdown("---")
            st.subheader("📖 Relevant Thirukkural Verses")
            st.info(
                f"Found {len(results)} highly relevant kurals "
                "using our enhanced RAG system"
            )
            for i, (kural, details) in enumerate(results):
                display_kural(
                    kural,
                    i,
                    show_transliteration=show_transliteration,
                    show_english=True,
                )
                render_match_details_expander(details)
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
        if st.button("Search", key="number_search"):
            if not kural_numbers_input.strip():
                st.warning("Please enter Kural numbers to search")
            else:
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


def _render_chapter_detail(chapter):
    """Render full detail for a single chapter."""
    kurals = chapter.get("Kurals", [])
    summary = chapter.get("Summary", [])

    st.markdown(f"### 📖 {chapter['Chapter']}")
    st.caption(f"{len(kurals)} kurals in this chapter")

    if summary:
        st.markdown("**Key Insights:**")
        for point in summary:
            st.markdown(f"- {point}")

    if kurals:
        st.markdown("---")
        st.markdown("**Kurals:**")
        for kural in kurals:
            num = kural.get("Number", "?")
            translation = kural.get("Translation", "")
            explanation = kural.get("Explanation", "")
            couplet = kural.get("Couplet", "")
            with st.expander(f"#{num} — {translation[:70]}{'…' if len(translation) > 70 else ''}"):
                st.markdown(f"**Translation:** {translation}")
                if explanation:
                    st.markdown(f"**Explanation:** {explanation}")
                if couplet:
                    st.markdown(f"**Couplet:** {couplet}")


def render_browse_summaries():
    st.markdown(
        '<h1 class="main-header">📖 Browse Chapters</h1>',
        unsafe_allow_html=True,
    )

    all_chapters = get_aggregated_chapters()
    if not all_chapters:
        st.warning("No chapters available in the aggregated database")
        return

    # Thirukkural sections by chapter index (0-based)
    SECTIONS = [
        ("📿 Virtue", 0, 38),    # chapters 1–38
        ("💰 Wealth", 38, 108),  # chapters 39–108
        ("💕 Love", 108, 133),   # chapters 109–133
    ]

    search = st.text_input(
        "🔍 Filter chapters by name:",
        placeholder="e.g., rain, friendship, leadership",
        key="browse_search",
    )
    search_lower = search.strip().lower()

    tab_labels = [s[0] for s in SECTIONS]
    tabs = st.tabs(tab_labels)

    for tab, (label, start, end) in zip(tabs, SECTIONS):
        section_chapters = all_chapters[start:end]
        if search_lower:
            section_chapters = [
                ch for ch in section_chapters
                if search_lower in ch["Chapter"].lower()
                or any(search_lower in pt.lower() for pt in ch.get("Summary", []))
            ]

        with tab:
            if not section_chapters:
                st.info(f"No chapters match '{search}' in this section.")
                continue

            chapter_names = [ch["Chapter"] for ch in section_chapters]
            session_key = f"browse_selected_{label}"

            # Preserve selection across reruns; reset if search changes
            prev_search_key = f"browse_prev_search_{label}"
            if st.session_state.get(prev_search_key) != search_lower:
                st.session_state[session_key] = chapter_names[0]
                st.session_state[prev_search_key] = search_lower

            selected_name = st.selectbox(
                "Choose a chapter:",
                options=chapter_names,
                key=session_key,
            )

            selected_chapter = next(
                (ch for ch in section_chapters if ch["Chapter"] == selected_name), None
            )
            if selected_chapter:
                st.markdown("---")
                _render_chapter_detail(selected_chapter)


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
        st.metric("AI Summary", "✓ Available")

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

    **Complete Thirukkural Coverage**
    All 1,330 verses are present — every couplet in Tamil, transliteration, and English,
    with meanings drawn from three classical Tamil commentators
    (மு.வரதராசனார், சாலமன் பாப்பையா, and மு.கருணாநிதி).

    **Ask Kural — Topic & Emotion Search**
    Describe a situation, ask a question, or name a theme. The app matches your words
    against verse content and chapter themes, then surfaces the most relevant kurals
    with a plain-English explanation of why each was chosen.

    **Explore Themes — Three Ways to Search**
    Browse by theme category, search by any keyword, or jump directly to a verse by number.
    Results show the full verse with match reasoning.

    **Browse Chapters — All 133 Chapters**
    Navigate the complete text organised into its three books — Virtue, Wealth, and Love.
    Each chapter includes a curated summary and every verse in full.

    **Optional AI Summary (Claude)**
    When you want deeper synthesis, enable the AI Summary on the Ask Kural page. Claude
    reads the retrieved verses and writes a concise, grounded response — always tied
    to the actual verse content, never invented.

    ### 📖 About Thirukkural

    Thirukkural is a classic Tamil text consisting of 1,330 couplets dealing with the everyday virtues of an individual.
    It is one of the most important works in Tamil literature and is considered a masterpiece of ethical literature.

    The text is divided into three books:
    - **Aram (Virtue)** — 38 chapters, 380 verses on moral and ethical life
    - **Porul (Wealth)** — 70 chapters, 700 verses on statecraft, economics, and conduct
    - **Inbam (Love)** — 25 chapters, 250 verses on human love and relationships

    ### 🔍 How KuralCompanion Works

    **Verse Search**
    Your query is broken into words and matched against four fields in every verse —
    the English translation, the meaning, the Tamil couplet, and the chapter theme.
    Each match contributes to a relevance score; the top five verses are returned.

    **Theme Detection**
    Before searching, your input is scanned against a curated list of theme keywords
    (wisdom, courage, friendship, love, leadership, and more). A theme match adds a
    stronger signal to the score, so topically aligned verses rank higher.

    **AI Synthesis (optional)**
    If the AI Summary option is enabled, the five retrieved verses are passed to Claude,
    which writes a 3–4 sentence synthesis grounded strictly in those verses.
    Responses are cached — the same query never calls the API twice.

    ### 📁 Data Sources

    The app draws from two complementary datasets:

    **Verse Database** — Three JSON files (`kural_database.json`, `comprehensive_kurals.json`,
    `extended_kurals.json`) covering all 1,330 kurals, each with Tamil lines, transliteration,
    English translation, meaning, three Tamil commentaries, couplet text, and emotion tags.

    **Chapter Summaries** — `aggregated_thirukkural_with_summary.json` holds all 133 chapters
    with curated key-insight bullets used in the Browse Chapters section.
    """
    )
