import feedparser
import hashlib
import time

from datetime import datetime
from backend.storage import save_signal


# =====================================================
# RSS SOURCES
# =====================================================
RSS_SOURCES = [
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
]


# =====================================================
# CACHE
# =====================================================
CACHE = {}
CACHE_TTL = 300


# =====================================================
# DUPLICATE CACHE
# =====================================================
SEEN = {}
DUP_TTL = 1800


# =====================================================
# SIGNAL KEYWORDS (RELAXED)
# =====================================================
KEYWORDS = [
    "ai", "technology", "tech",
    "market", "economy", "stock",
    "war", "conflict", "crisis",
    "security", "cyber",
    "energy", "oil",
    "politics", "china", "usa", "europe"
]


# =====================================================
# HASH
# =====================================================
def make_hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


# =====================================================
# DUPLICATE CHECK (SAFE)
# =====================================================
def is_duplicate(text: str) -> bool:
    h = make_hash(text)
    now = time.time()

    if h in SEEN and now - SEEN[h] < DUP_TTL:
        return True

    SEEN[h] = now

    # memory cleanup
    if len(SEEN) > 5000:
        SEEN.clear()

    return False


# =====================================================
# CACHE FEED
# =====================================================
def get_feed(url: str):
    now = time.time()

    if url in CACHE:
        cached_time, cached_feed = CACHE[url]
        if now - cached_time < CACHE_TTL:
            return cached_feed

    feed = feedparser.parse(url)

    CACHE[url] = (now, feed)
    return feed


# =====================================================
# SIGNAL CHECK (RELAXED + SAFE FALLBACK)
# =====================================================
def is_signal(title: str, content: str) -> bool:
    text = f"{title} {content}".lower()

    keyword_hit = any(k in text for k in KEYWORDS)

    # fallback: long meaningful content still counts
    fallback = len(text) > 120

    return keyword_hit or fallback


# =====================================================
# SCORE ENGINE
# =====================================================
def calculate_score(title: str, content: str) -> float:
    text = f"{title} {content}".lower()

    score = 0.5

    high = ["war", "conflict", "crisis", "attack", "collapse"]
    medium = ["ai", "market", "economy", "energy", "security"]

    for w in high:
        if w in text:
            score += 1.0

    for w in medium:
        if w in text:
            score += 0.4

    return round(min(score, 2.5), 2)


# =====================================================
# MAIN CRAWLER
# =====================================================
def crawl():
    results = []

    for url in RSS_SOURCES:

        try:
            feed = get_feed(url)

            if not feed.entries:
                continue

            for entry in feed.entries[:15]:

                title = (entry.get("title") or "").strip()
                content = (
                    entry.get("summary")
                    or entry.get("description")
                    or ""
                ).strip()

                if not title:
                    continue

                full_text = f"{title} {content}"

                # duplicate filter
                if is_duplicate(full_text):
                    continue

                # signal filter (RELAXED)
                if not is_signal(title, content):
                    continue

                score = calculate_score(title, content)

                item = {
                    "title": title,
                    "topic": title,
                    "text": content or title,
                    "score": score,
                    "sources": [url],
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }

                # DB SAVE (SAFE STRUCTURE)
                try:
                    save_signal({
                        "title": item["title"],
                        "topic": item["topic"],
                        "content": item["text"],
                        "priority": item["score"],
                        "published": 1,
                        "timestamp": int(time.time())
                    })
                except Exception as e:
                    print("[DB ERROR]", e)

                results.append(item)

        except Exception as e:
            print("[RSS ERROR]", url, e)

    print("[CRAWLER DONE]", len(results))

    return results
