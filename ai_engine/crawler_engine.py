import feedparser
import hashlib
import time
from datetime import datetime

from ai_engine.signal_radar import radar


SOURCES = [
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "https://www.theverge.com/rss/index.xml"
]


KEYWORDS = [
    "ai",
    "technology",
    "chip",
    "semiconductor",
    "supply chain",
    "energy",
    "war",
    "conflict"
]


SEEN_HASHES = set()

CACHE = {}

CACHE_TTL = 300


def make_hash(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def get_feed(url):

    now = time.time()

    if url in CACHE:

        cached_time, cached_feed = CACHE[url]

        if now - cached_time < CACHE_TTL:
            return cached_feed

    feed = feedparser.parse(url)

    CACHE[url] = (now, feed)

    return feed


def is_signal(title, summary):

    text = (title + " " + summary).lower()

    for keyword in KEYWORDS:
        if keyword in text:
            return True

    return False


def crawl():

    results = []

    for url in SOURCES:

        try:

            feed = get_feed(url)

            for entry in feed.entries[:5]:

                title = entry.get("title", "")
                summary = entry.get("summary", "")

                fingerprint = make_hash(title + summary)

                if fingerprint in SEEN_HASHES:
                    continue

                SEEN_HASHES.add(fingerprint)

                if not is_signal(title, summary):
                    continue

                signal = {
                    "title": title,
                    "score": 60,
                    "lat": 0,
                    "lon": 0,
                    "timestamp": datetime.utcnow().isoformat()
                }

                radar.push(signal)

                results.append(signal)

        except Exception as e:

            print("crawler error:", e)

    print("crawler collected:", len(results))

    return results


