import feedparser
import hashlib
import time

from backend.storage import save_post  # 🔥 KRİTİK

RSS_SOURCES = [

    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",

    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://feeds.bbci.co.uk/news/technology/rss.xml",

    "https://www.aljazeera.com/xml/rss/all.xml",

    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",

    "https://www.reddit.com/r/worldnews/.rss",
    "https://www.reddit.com/r/technology/.rss"
]


SEEN = set()
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

    feed = feedparser.parse(url, request_headers={
        "User-Agent": "Mozilla/5.0"
    })

    CACHE[url] = (now, feed)

    return feed


def crawl():

    results = []

    for url in RSS_SOURCES:

        try:
            feed = get_feed(url)

            print(f"[CRAWL] {url} entries:", len(feed.entries))

            for entry in feed.entries[:5]:

                title = entry.get("title", "").strip()
                content = entry.get("summary", entry.get("description", "")).strip()

                if not title:
                    continue

                fingerprint = make_hash(title + content)

                if fingerprint in SEEN:
                    continue

                SEEN.add(fingerprint)

                item = {
                    "title": title,
                    "content": content if content else title,
                    "source": url,
                    "timestamp": time.time()
                }

                # 🔥 DB'YE YAZ (ASIL FIX)
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

    
