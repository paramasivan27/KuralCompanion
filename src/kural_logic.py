"""Kural search and relevance logic (RAG, theme detection, counts)."""

import os

import anthropic
import streamlit as st

from app_state import COMPREHENSIVE_KURAL_DATABASE, THEME_KEYWORDS


def detect_theme(text):
    """Detect theme from user input."""
    text_lower = text.lower()
    detected_themes = []
    for theme, keywords in THEME_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                detected_themes.append(theme)
                break
    return detected_themes[:2] if detected_themes else ["wisdom"]


def find_relevant_kurals_rag(user_input, themes):
    """Find relevant kurals using RAG: theme + content scoring."""
    detected_themes = [t.lower() for t in themes]
    search_terms = [
        term.lower().strip()
        for term in user_input.lower().split()
        if len(term.strip()) > 2
    ]
    scored = []

    for db_theme, kurals in COMPREHENSIVE_KURAL_DATABASE.items():
        for kural in kurals:
            score = 0
            match_details = []
            db_theme_lower = db_theme.lower()

            for theme in detected_themes:
                if theme == db_theme_lower:
                    score += 15
                    match_details.append(f"Exact theme match: {db_theme}")
                elif theme in db_theme_lower or db_theme_lower in theme:
                    score += 12
                    match_details.append(f"Partial theme match: {db_theme}")

            english_text = kural.get("english", "").lower()
            english_matches = [t for t in search_terms if t in english_text]
            if english_matches:
                score += sum(min(len(t), 5) for t in english_matches)
                match_details.append(f"English matches: {', '.join(english_matches)}")

            meaning_text = kural.get("meaning", "").lower()
            meaning_matches = [t for t in search_terms if t in meaning_text]
            if meaning_matches:
                score += sum(min(len(t), 5) for t in meaning_matches)
                match_details.append(f"Meaning matches: {', '.join(meaning_matches)}")

            couplet_text = kural.get("couplet", "").lower()
            couplet_matches = [t for t in search_terms if t in couplet_text]
            if couplet_matches:
                score += sum(min(len(t), 4) for t in couplet_matches)
                match_details.append(f"Couplet matches: {', '.join(couplet_matches)}")

            if score > 0:
                if len(match_details) >= 4:
                    score += 5
                elif len(match_details) >= 3:
                    score += 3
                if any("Exact theme match" in d for d in match_details):
                    if any("English matches" in d or "Meaning matches" in d for d in match_details):
                        score += 5

            if score >= 5:
                scored.append((score, kural, match_details))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [(kural, details) for _, kural, details in scored[:5]]


def find_kurals_by_keywords(keywords):
    """Find kurals by keywords using RAG."""
    search_keywords = [kw.lower().strip() for kw in keywords.split() if kw.strip()]
    if not search_keywords:
        return []
    mock_input = " ".join(search_keywords)
    themes = detect_theme(mock_input)
    relevant = find_relevant_kurals_rag(mock_input, themes)
    return [kural for kural, _ in relevant]


def get_total_kural_count():
    """Total number of kurals in the comprehensive database."""
    return sum(len(kurals) for kurals in COMPREHENSIVE_KURAL_DATABASE.values())


def get_theme_counts():
    """Count of kurals per theme."""
    return {theme: len(kurals) for theme, kurals in COMPREHENSIVE_KURAL_DATABASE.items()}


def generate_contextual_response(user_input, themes, kurals_with_details):
    """Generate a short contextual response for the user based on RAG results."""
    parts = []
    parts.append(
        "Thirukkural's timeless wisdom offers profound guidance for your question. "
        "Let me share the most relevant verses that directly address your inquiry."
    )
    if themes:
        if len(themes) == 1:
            parts.append(
                f"The theme of {themes[0]} is deeply explored in these ancient verses, "
                "offering practical wisdom for modern life."
            )
        else:
            parts.append(
                f"The themes of {', '.join(themes[:-1])} and {themes[-1]} are beautifully "
                "interconnected in Thirukkural, providing comprehensive guidance."
            )
    if kurals_with_details:
        numbers = [k.get("number", "Unknown") for k, _ in kurals_with_details]
        if len(numbers) == 1:
            parts.append(f"I've found Kural #{numbers[0]}, which directly addresses your question.")
        else:
            parts.append(
                f"I've found {len(numbers)} highly relevant kurals "
                f"(#{', '.join(map(str, numbers))}) that directly address your question."
            )
        parts.append(
            "These verses were selected because they address your themes and "
            "contain content that directly relates to your question."
        )
        details_flat = [d for _, details in kurals_with_details for d in details]
        unique = set(d.split(":")[0].strip() for d in details_flat if "match" in d.lower())
        if unique:
            parts.append(f"The relevance comes from {', '.join(list(unique)[:3])}.")
    parts.append(
        "Thirukkural's wisdom is timeless because it addresses the fundamental "
        "aspects of human experience that remain constant across generations."
    )
    return " ".join(parts)


def llm_available():
    """Return True if the Anthropic API key is configured."""
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


@st.cache_data(show_spinner=False)
def generate_llm_summary(user_input, kurals_tuple):
    """Call Claude Haiku to synthesize the retrieved kurals for the user's query.

    kurals_tuple is a tuple-of-tuples so Streamlit can cache it (lists aren't hashable).
    Each inner tuple is (english, meaning, number).
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None

    kural_lines = "\n".join(
        f"- Kural #{num}: \"{english}\" — {meaning}"
        for english, meaning, num in kurals_tuple
    )

    prompt = f"""You are a knowledgeable guide to Thirukkural, the ancient Tamil text of wisdom written by Thiruvalluvar.

A user asked: "{user_input}"

The following Thirukkural verses were retrieved as most relevant:
{kural_lines}

In 3-4 sentences, synthesize what Thiruvalluvar teaches about this topic across these specific verses. \
Be concrete — reference the verse numbers and their ideas. Do not invent content beyond what the verses say."""

    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text
