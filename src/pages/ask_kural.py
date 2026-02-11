"""Ask Kural page."""

import streamlit as st

from kural_logic import detect_theme, find_relevant_kurals_rag, generate_contextual_response
from ui_components import (
    display_kural,
    render_match_details_expander,
    render_display_options_expander,
)


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
                st.markdown(f"""
                **Your Question:** "{user_input}"

                **KuralCompanion's Response:** {contextual_response}
                """)
                st.markdown("---")
                st.subheader("📖 Relevant Thirukkural Verses")
                st.info(
                    f"Found {len(relevant_kurals_with_details)} highly relevant kurals "
                    "using our enhanced RAG system"
                )
                for i, (kural, details) in enumerate(relevant_kurals_with_details):
                    display_kural(kural, i, show_transliteration=show_transliteration, show_english=True)
                    render_match_details_expander(details)
            else:
                st.warning(
                    "No relevant Kurals found for your query. "
                    "Try using different keywords or rephrasing your question."
                )
                st.info(
                    "💡 Tip: Try using more specific words or describing your topic in detail for better matches."
                )
