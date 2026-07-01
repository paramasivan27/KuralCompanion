"""
KuralCompanion - Ancient Wisdom for Modern Life.
Main entry point; delegates to modular pages and shared components.
"""

import streamlit as st
from streamlit_option_menu import option_menu

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
    clear_emotion_related_state()
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "Home"

    st.set_page_config(**PAGE_CONFIG)
    st.markdown(get_app_css(), unsafe_allow_html=True)

    with st.sidebar:
        st.markdown(
            "<h2 style='color:#D4AF37;font-family:\"EB Garamond\",serif;"
            "text-align:center;letter-spacing:0.05em;margin-bottom:0.2rem;'>"
            "🌟 KuralCompanion</h2>"
            "<p style='color:#9A8A70;font-family:\"EB Garamond\",serif;"
            "text-align:center;font-style:italic;font-size:0.9rem;margin-top:0;'>"
            "Ancient Wisdom for Modern Life</p>"
            "<hr style='border:none;border-top:1px solid #6B2525;margin:0.8rem 0;'>",
            unsafe_allow_html=True,
        )
        sidebar_selected = option_menu(
            menu_title=None,
            options=[o[0] for o in SIDEBAR_OPTIONS],
            icons=[o[1] for o in SIDEBAR_OPTIONS],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"background-color": "#2B0A0A", "padding": "4px"},
                "nav-link": {
                    "font-family": '"EB Garamond", serif',
                    "font-size": "1.05rem",
                    "color": "#C9B99A",
                    "border-radius": "4px",
                },
                "nav-link-selected": {
                    "background-color": "#5C1A1A",
                    "color": "#D4AF37",
                    "font-weight": "600",
                    "border-left": "3px solid #D4AF37",
                },
                "icon": {"color": "#D4AF37"},
            },
        )

    if "last_sidebar_selection" not in st.session_state:
        st.session_state.last_sidebar_selection = sidebar_selected

    if sidebar_selected != st.session_state.last_sidebar_selection:
        st.session_state.selected_page = sidebar_selected
        st.session_state.last_sidebar_selection = sidebar_selected
        clear_page_state()
        st.rerun()

    selected = st.session_state.selected_page
    if selected not in VALID_PAGES:
        st.session_state.selected_page = "Home"
        selected = "Home"
        st.rerun()

    main_container = st.container()
    with main_container:
        if selected == "Home":
            render_home()
        elif selected == "Ask Kural":
            render_ask_kural()
        elif selected == "Explore Themes":
            render_explore_themes()
        elif selected == "Browse Chapter Summaries":
            render_browse_summaries()
        elif selected == "About":
            render_about()
        else:
            st.error("Page not found. Please select a valid page from the sidebar.")


if __name__ == "__main__":
    main()
