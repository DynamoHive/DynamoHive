import feedparser
import hashlib
import time

from datetime import datetime

from ai_engine.signal_radar import radar


# -------------------------
# FEED SOURCES
# -------------------------
SOURCES = [
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "https://www.theverge.com/rss/index.xml"
]


# -------------------------
# SIGNAL KEYWORDS
# -------------------------
KEYWORDS = [
    "ai",
    "technology",
    "chip",
    "semiconductor",
    "supply chain",
    "energy",
    "war",
    "conflict",
    "cyber",
    "security",
    "crisis",
    "market"
]


# -------------------------
# CACHE + DEDUP
# -------------------------
SEEN_HASHES = set()

CACHE = {}

CACHE_TTL = 300


# -------------------------
# HASHING
# -------------------------
def make_hash(text):

    return hashlib.md5(
        text.encode("utf-8")
    ).hexdigest()


# -------------------------
# FEED CACHE
# -------------------------
def get_feed(url):

    now = time.time()

    if url in CACHE:

        cached_time, cached_feed = CACHE[url]

        if now - cached_time < CACHE_TTL:
            return cached_feed

    parsed_feed = feedparser.parse(url)

    CACHE[url] = (
        now,
        parsed_feed
    )

    return parsed_feed


# -------------------------
# SIGNAL DETECTION
# -------------------------
def is_signal(title, summary):

    text = f"{title} {summary}".lower()

    return any(
        keyword in text
        for keyword in KEYWORDS
    )


# -------------------------
# SCORE ENGINE
# -------------------------
def calculate_score(title, summary):

    text = f"{title} {summary}".lower()

    score = 0.5

    high_impact = [
        "war",
        "crisis",
        "conflict",
        "collapse",
        "cyberattack"
    ]

    medium_impact = [
        "ai",
        "market",
        "energy",
        "security",
        "chip"
    ]

    for word in high_impact:
        if word in text:
            score += 1.0

    for word in medium_impact:
        if word in text:
            score += 0.4

    return round(score, 2)


# -------------------------
# MAIN CRAWLER
# -------------------------
def crawl():

    results = []

    for url in SOURCES:

        try:

            feed = get_feed(url)

            for entry in feed.entries[:10]:

                title = entry.get("title", "")
                summary = entry.get("summary", "")

                fingerprint = make_hash(
                    title + summary
                )

                if fingerprint in SEEN_HASHES:
                    continue

                SEEN_HASHES.add(fingerprint)

                if not is_signal(title, summary):
                    continue

                score = calculate_score(
                    title,
                    summary
                )

                signal = {
                    "topic": title,
                    "text": summary,
                    "score": score,
                    "sources": [url],
                    "lat": 0,
                    "lon": 0,
                    "timestamp": (
                        datetime.utcnow().isoformat() + "Z"
                    )
                }

                radar.push(signal)

                results.append(signal)

        except Exception as e:

            print("crawler error:", e)

    print("crawler collected:", len(results))

    return results

