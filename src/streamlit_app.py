"""
KuralCompanion - Ancient Wisdom for Modern Life.
Main entry point; delegates to modular pages and shared components.
"""

import streamlit as st

from config import PAGE_CONFIG, SIDEBAR_OPTIONS, VALID_PAGES
from styles import get_app_css
from ui_components import clear_emotion_related_state, clear_page_state
from kural_pages import (
    render_home,
    render_ask_kural,
    render_explore_themes,
    render_browse_summaries,
    render_about,
)


def main():
    st.set_page_config(**PAGE_CONFIG)
    st.markdown(get_app_css(), unsafe_allow_html=True)

    clear_emotion_related_state()
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "Home"

    current_page = st.session_state.selected_page
    if current_page not in VALID_PAGES:
        current_page = "Home"
        st.session_state.selected_page = "Home"

    with st.sidebar:
        st.markdown(
            "<h2 style='color:#D4AF37;font-family:\"EB Garamond\",serif;"
            "text-align:center;letter-spacing:0.05em;margin-bottom:0.2rem;'>"
            "🌟 KuralCompanion</h2>"
            "<p style='color:#C9B99A;font-family:\"EB Garamond\",serif;"
            "text-align:center;font-style:italic;font-size:0.9rem;margin-top:0;'>"
            "Ancient Wisdom for Modern Life</p>"
            "<hr style='border:none;border-top:1px solid #6B2525;margin:0.8rem 0;'>",
            unsafe_allow_html=True,
        )
        for page_name, emoji in SIDEBAR_OPTIONS:
            is_active = current_page == page_name
            if st.button(
                f"{emoji}  {page_name}",
                key=f"nav_{page_name}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                if not is_active:
                    st.session_state.selected_page = page_name
                    clear_page_state()
                    st.rerun()

    renderers = {
        "Home": render_home,
        "Ask Kural": render_ask_kural,
        "Explore Themes": render_explore_themes,
        "Browse Chapters": render_browse_summaries,
        "About": render_about,
    }
    renderers.get(current_page, render_home)()


if __name__ == "__main__":
    main()
