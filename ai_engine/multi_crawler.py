import feedparser
import hashlib
import time

from backend.storage import save_post


# -------------------------
# 🔥 SOURCES
# -------------------------
RSS_SOURCES = [
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
]


# -------------------------
# 🔥 CACHE (FEED)
# -------------------------
CACHE = {}
CACHE_TTL = 300  # 5 min


# -------------------------
# 🔥 DUPLICATE CACHE
# -------------------------
SEEN_HASHES = {}
DUP_TTL = 1800  # 30 min


# -------------------------
# 🔧 HELPERS
# -------------------------
def make_hash(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def is_duplicate(text):
    h = make_hash(text)
    now = time.time()

    if h in SEEN_HASHES:
        if now - SEEN_HASHES[h] < DUP_TTL:
            return True

    SEEN_HASHES[h] = now
    return False


def get_feed(url):

    now = time.time()

    if url in CACHE:
        cached_time, cached_feed = CACHE[url]
        if now - cached_time < CACHE_TTL:
            return cached_feed

    feed = feedparser.parse(url, request_headers={
        "User-Agent": "Mozilla/5.0"
    })

    CACHE[url] = (now, feed)

    return feed


# -------------------------
# 🚀 MAIN CRAWLER
# -------------------------
def crawl():

    results = []

    for url in RSS_SOURCES:

        try:
            feed = get_feed(url)

            print(f"[CRAWL] {url} entries:", len(feed.entries))

            if not feed.entries:
                continue

            for entry in feed.entries[:5]:

                title = entry.get("title", "").strip()
                content = entry.get("summary") or entry.get("description") or ""

                if not title:
                    continue

                text = f"{title} {content}"

                # 🔥 DUPLICATE FILTER
                if is_duplicate(text):
                    continue

                item = {
                    "title": title,
                    "content": content.strip() if content else title,
                    "source": url,
                    "timestamp": time.time()
                }

                # 🔥 DB WRITE
                try:
                    save_post(item["title"], item["content"])
                except Exception as db_error:
                    print("DB write error:", db_error)

                results.append(item)

                print("ADD:", title[:60])

        except Exception as e:
            print("rss error:", url, e)

    print("crawler collected:", len(results))

    return results

    
