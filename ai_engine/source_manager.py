sources = [
    {"type": "rss", "url": "https://news.google.com/rss"},
    {"type": "rss", "url": "https://www.aljazeera.com/xml/rss/all.xml"},
]


def get_sources():
    return sources

crawler içinde:

from ai_engine.source_manager import get_sources

ve:
