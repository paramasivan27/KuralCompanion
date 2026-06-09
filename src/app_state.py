"""Application state: merged kural database and lookup helpers."""

from kural_database import KURAL_DATABASE, THEME_KEYWORDS

COMPREHENSIVE_KURAL_DATABASE = KURAL_DATABASE


def get_kural_by_number_comprehensive(number):
    """Get a kural by its number from the comprehensive database."""
    for theme, kurals in COMPREHENSIVE_KURAL_DATABASE.items():
        for kural in kurals:
            if kural.get("number") == number:
                return kural
    return None


def get_sample_kural():
    """Return a sample kural for reading display options (e.g. mv/sp/mk)."""
    for theme, kurals in COMPREHENSIVE_KURAL_DATABASE.items():
        if kurals:
            return kurals[0]
    return None
