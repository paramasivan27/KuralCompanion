"""Browse Chapter Summaries page."""

import streamlit as st

from aggregated_kurals import get_aggregated_chapters


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
            or any(
                search_lower in point.lower()
                for point in ch.get("Summary", [])
            )
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
                        for k, kural in enumerate(chapter["Kurals"][:5]):
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
