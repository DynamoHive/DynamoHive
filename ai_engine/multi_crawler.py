import feedparser
import hashlib
import time

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

    feed = feedparser.parse(url)

    CACHE[url] = (now, feed)

    return feed


def crawl():

    results = []

    for url in RSS_SOURCES:

        try:

            feed = get_feed(url)

            for entry in feed.entries[:5]:

                title = entry.get("title", "")
                content = entry.get("summary", entry.get("description", ""))

                fingerprint = make_hash(title + content)

                if fingerprint in SEEN:
                    continue

                SEEN.add(fingerprint)

                results.append({

                    "title": title,
                    "content": content,
                    "source": url,
                    "timestamp": time.time()

                })

        except Exception as e:

            print("rss error:", e)

    print("crawler collected:", len(results))

    return results

    
