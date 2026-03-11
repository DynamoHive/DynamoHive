import feedparser
import hashlib
import time


SOURCES = [
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "https://www.theverge.com/rss/index.xml"
]


# daha önce görülen içerikler
SEEN_HASHES = set()

# RSS cache
CACHE = {}

# cache süresi (5 dakika)
CACHE_TTL = 300


def make_hash(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def get_feed(url):

    now = time.time()

    # cache kontrol
    if url in CACHE:

        cached_time, cached_feed = CACHE[url]

        if now - cached_time < CACHE_TTL:
            return cached_feed

    feed = feedparser.parse(url)

    CACHE[url] = (now, feed)

    return feed


def crawl():

    results = []

    for url in SOURCES:

        try:

            feed = get_feed(url)

            for entry in feed.entries[:5]:

                title = entry.get("title", "")
                summary = entry.get("summary", "")

                fingerprint = make_hash(title + summary)

                # dedup kontrol
                if fingerprint in SEEN_HASHES:
                    continue

                SEEN_HASHES.add(fingerprint)

                results.append({
                    "title": title,
                    "content": summary,
                    "source": url
                })

        except Exception as e:

            print("crawler error:", e)

    print("crawler collected:", len(results))

    return results
