"""Explore Themes page: search by theme, keyword, or kural number."""

import streamlit as st

from app_state import COMPREHENSIVE_KURAL_DATABASE, get_kural_by_number_comprehensive
from kural_logic import detect_theme, find_relevant_kurals_rag
from ui_components import (
    display_kural,
    render_match_details_expander,
    render_display_options_expander,
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
                display_kural(kural, show_transliteration=show_transliteration, show_english=True)
                st.markdown("<br>", unsafe_allow_html=True)

    elif search_option == "Keyword":
        keyword = st.text_input(
            "Enter a keyword to search in kurals:", key="theme_keyword_search"
        )
        if st.button("Search", key="keyword_search") and keyword:
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
        elif st.button("Search", key="keyword_search"):
            st.warning("Please enter a keyword to search")

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
                        k = get_kural_by_number_comprehensive(num)
                        if k:
                            found.append(k)
                        else:
                            st.warning(f"Kural #{num} not found in the current database")
                    if found:
                        st.info(f"Found {len(found)} out of {len(kural_numbers)} requested kurals")
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
