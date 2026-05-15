import feedparser
import hashlib
import time
from datetime import datetime

from backend.storage import save_signal


# =====================================================
# SOURCES
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
# DUPLICATE
# =====================================================
SEEN = {}
DUP_TTL = 1800


# =====================================================
# KEYWORDS (soft signal mode)
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
# DUPLICATE CHECK (safe)
# =====================================================
def is_duplicate(text: str) -> bool:
    h = make_hash(text)
    now = time.time()

    last = SEEN.get(h)
    if last and now - last < DUP_TTL:
        return True

    SEEN[h] = now

    if len(SEEN) > 5000:
        SEEN.clear()

    return False


# =====================================================
# FEED CACHE
# =====================================================
def get_feed(url: str):
    now = time.time()

    if url in CACHE:
        t, feed = CACHE[url]
        if now - t < CACHE_TTL:
            return feed

    try:
        feed = feedparser.parse(url)
    except Exception:
        return None

    CACHE[url] = (now, feed)
    return feed


# =====================================================
# SIGNAL CHECK (FIXED BALANCE)
# =====================================================
def is_signal(title: str, content: str) -> bool:
    text = f"{title} {content}".lower()

    keyword_hit = any(k in text for k in KEYWORDS)

    # IMPORTANT FIX:
    # fallback too aggressive before → now limited
    fallback = len(text) > 180

    return keyword_hit or fallback


# =====================================================
# SCORE ENGINE
# =====================================================
def calculate_score(title: str, content: str) -> float:
    text = f"{title} {content}".lower()

    score = 0.4  # slightly lower baseline

    high = ["war", "conflict", "crisis", "attack", "collapse"]
    medium = ["ai", "market", "economy", "energy", "security"]

    for w in high:
        if w in text:
            score += 0.9

    for w in medium:
        if w in text:
            score += 0.35

    return round(min(score, 2.2), 2)


# =====================================================
# MAIN CRAWLER
# =====================================================
def crawl():

    results = []

    for url in RSS_SOURCES:

        feed = get_feed(url)

        if not feed or not hasattr(feed, "entries"):
            continue

        entries = feed.entries[:12]  # safer cap

        for entry in entries:

            title = (entry.get("title") or "").strip()
            content = (
                entry.get("summary")
                or entry.get("description")
                or ""
            ).strip()

            if not title:
                continue

            full_text = f"{title} {content}"

            if is_duplicate(full_text):
                continue

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

            try:
                save_signal({
                    "title": title,
                    "topic": title,
                    "content": item["text"],
                    "priority": score,
                    "published": 1,
                    "timestamp": int(time.time())
                })
            except Exception:
                pass

            results.append(item)

    print("[CRAWLER DONE]", len(results))
    return results
