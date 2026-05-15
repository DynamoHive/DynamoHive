import feedparser
import hashlib
import time
from datetime import datetime

from backend.storage import save_signal
from backend.logger import logger


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


CACHE = {}
CACHE_TTL = 300

SEEN = {}
DUP_TTL = 1800


KEYWORDS = [
    "ai", "technology", "tech",
    "market", "economy", "stock",
    "war", "conflict", "crisis",
    "security", "cyber",
    "energy", "oil",
    "politics", "china", "usa", "europe"
]


# =====================================================
def make_hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


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
def get_feed(url: str):
    now = time.time()

    if url in CACHE:
        t, feed = CACHE[url]
        if now - t < CACHE_TTL:
            return feed

    feed = feedparser.parse(url)

    # 🔥 DEBUG FIX
    if getattr(feed, "bozo", False):
        logger.warning(f"[FEED ISSUE] {url}")

    CACHE[url] = (now, feed)
    return feed


# =====================================================
def is_signal(title: str, content: str) -> bool:
    text = f"{title} {content}".lower()

    # 🔥 FIX: softer logic
    if any(k in text for k in KEYWORDS):
        return True

    # fallback ONLY if title strong
    return len(title) > 40


# =====================================================
def calculate_score(title: str, content: str) -> float:
    text = f"{title} {content}".lower()

    score = 0.4

    high = ["war", "conflict", "crisis", "attack", "collapse"]
    medium = ["ai", "market", "economy", "energy", "security"]

    for w in high:
        if w in text:
            score += 0.8

    for w in medium:
        if w in text:
            score += 0.3

    return round(min(score, 2.2), 2)


# =====================================================
def crawl():

    results = []

    for url in RSS_SOURCES:

        try:
            feed = get_feed(url)

            if not feed or not getattr(feed, "entries", None):
                continue

            entries = feed.entries[:15]

            for entry in entries:

                title = (entry.get("title") or "").strip()

                content = (
                    entry.get("summary")
                    or entry.get("description")
                    or entry.get("content", [{}])[0].get("value")
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

        except Exception as e:
            logger.error(f"[CRAWLER ERROR] {url}: {e}")

    logger.info(f"[CRAWLER DONE] {len(results)}")
    return results
