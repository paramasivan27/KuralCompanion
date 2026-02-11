"""Application state: merged kural database and lookup helpers."""

from kural_database import KURAL_DATABASE, THEME_KEYWORDS
from comprehensive_kurals import KURAL_DATABASE as COMPREHENSIVE_KURALS
from extended_kurals import KURAL_DATABASE as EXTENDED_KURALS


def merge_all_kural_databases(core_db, comprehensive_db, extended_db):
    """Merge all three kural databases into one comprehensive database."""
    merged_db = {}
    for theme, kurals in core_db.items():
        merged_db[theme] = list(kurals)
    for theme, kurals in comprehensive_db.items():
        if theme in merged_db:
            merged_db[theme].extend(kurals)
        else:
            merged_db[theme] = list(kurals)
    for theme, kurals in extended_db.items():
        if theme in merged_db:
            merged_db[theme].extend(kurals)
        else:
            merged_db[theme] = list(kurals)
    return merged_db


COMPREHENSIVE_KURAL_DATABASE = merge_all_kural_databases(
    KURAL_DATABASE, COMPREHENSIVE_KURALS, EXTENDED_KURALS
)


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
