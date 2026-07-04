"""Reusable UI components: kural card, session state helpers, display options."""

import streamlit as st

from kural_database import get_sample_kural


def get_available_explanations():
    """Return list of (display_name, key) for Tamil explanations (mv, sp, mk)."""
    sample = get_sample_kural()
    if not sample:
        return []
    out = []
    if sample.get("mv"):
        out.append(("மு.வரதராசனார்", "mv"))
    if sample.get("sp"):
        out.append(("சாலமன் பாப்பையா", "sp"))
    if sample.get("mk"):
        out.append(("மு.கருணாநிதி", "mk"))
    return out


def display_kural(kural, index=0, show_transliteration=True, show_english=True):
    """Render a single kural card. Tamil always shown; transliteration/English optional."""
    tamil_text = (
        f"{kural.get('line1', '')}<br>{kural.get('line2', '')}"
        if "line1" in kural
        else kural.get("tamil", "")
    )
    transliteration_text = ""
    if show_transliteration and kural.get("transliteration"):
        parts = kural["transliteration"].split(" ", 1)
        transliteration_text = (
            f"{parts[0]}<br>{parts[1]}" if len(parts) > 1 else kural["transliteration"]
        )

    mv = kural.get("mv", "")
    sp = kural.get("sp", "")
    mk = kural.get("mk", "")
    explanations_html = ""
    if mv or sp or mk:
        explanations_html = "<p><strong>Tamil Explanations:</strong></p>"
        key = st.session_state.get("selected_explanation")
        if key == "mv" and mv:
            explanations_html += f"<p><em>மு.வரதராசனார்:</em><br><span class='tamil-text'>{mv}</span></p>"
        elif key == "sp" and sp:
            explanations_html += f"<p><em>சாலமன் பாப்பையா:</em><br><span class='tamil-text'>{sp}</span></p>"
        elif key == "mk" and mk:
            explanations_html += f"<p><em>மு.கருணாநிதி:</em><br><span class='tamil-text'>{mk}</span></p>"
        else:
            if mv:
                explanations_html += f"<p><em>மு.வரதராசனார்:</em><br><span class='tamil-text'>{mv}</span></p>"
            elif sp:
                explanations_html += f"<p><em>சாலமன் பாப்பையா:</em><br><span class='tamil-text'>{sp}</span></p>"
            elif mk:
                explanations_html += f"<p><em>மு.கருணாநிதி:</em><br><span class='tamil-text'>{mk}</span></p>"

    sections = [
        f"<p><strong>Tamil:</strong><br><span class='tamil-text'>{tamil_text}</span></p>"
    ]
    if show_transliteration and transliteration_text:
        sections.append(f"<p><strong>Transliteration:</strong><br>{transliteration_text}</p>")
    if show_english:
        sections.append(f"<p><strong>English:</strong> {kural.get('english', '')}</p>")
    sections.append(f"<p><strong>Meaning:</strong> {kural.get('meaning', '')}</p>")
    if explanations_html:
        sections.append(explanations_html)

    st.markdown(
        f"""
        <div class="kural-card">
            <div class="kural-number">Kural #{kural.get('number', '')}</div>
            {''.join(sections)}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_match_details_expander(details, label_suffix=""):
    """Render an expander showing why a kural was matched."""
    count = sum(1 for d in details if "match" in d.lower())
    with st.expander(f"🔍 Why this Kural is relevant ({count} matches){label_suffix}"):
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


def render_display_options_expander(key_prefix=""):
    """
    Render display options (transliteration + Tamil explanation choice).
    Returns (show_transliteration,).
    """
    with st.expander("⚙️ Display Options", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            show_transliteration = st.checkbox(
                "Show Transliteration", value=True, key=f"{key_prefix}_translit"
            )
        with col2:
            available = get_available_explanations()
            if len(available) > 1:
                selected = st.radio(
                    "Choose Tamil explanation:",
                    options=[e[0] for e in available],
                    key=f"{key_prefix}_explanation",
                )
                for name, k in available:
                    if name == selected:
                        st.session_state.selected_explanation = k
                        break
            elif len(available) == 1:
                st.session_state.selected_explanation = available[0][1]
                st.info(f"Available: {available[0][0]}")
            else:
                st.session_state.selected_explanation = None
                st.info("No Tamil explanations available")
    st.session_state.show_transliteration = show_transliteration
    return show_transliteration


def clear_page_state():
    """Clear page-related session state for clean navigation."""
    for key in ["user_input", "search_results", "theme_analysis", "show_transliteration", "selected_explanation"]:
        if key in st.session_state:
            del st.session_state[key]


def clear_emotion_related_state():
    """Clear old emotion-related session state."""
    for key in [
        "emotions_user_input",
        "emotions_translit",
        "emotions_explanation",
        "emotion_analysis",
        "detected_emotions",
    ]:
        if key in st.session_state:
            del st.session_state[key]
