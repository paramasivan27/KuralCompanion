"""Page renderers for KuralCompanion."""

from pages.home import render_home
from pages.ask_kural import render_ask_kural
from pages.explore_themes import render_explore_themes
from pages.browse_summaries import render_browse_summaries
from pages.about import render_about

__all__ = [
    "render_home",
    "render_ask_kural",
    "render_explore_themes",
    "render_browse_summaries",
    "render_about",
]
