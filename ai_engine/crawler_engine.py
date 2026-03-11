import feedparser
import hashlib

SOURCES = [
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "https://www.theverge.com/rss/index.xml"
]

# Daha önce görülen içerikleri tutar
SEEN_HASHES = set()


def make_hash(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def crawl():

    results = []

    for url in SOURCES:

        try:
            feed = feedparser.parse(url)

            for entry in feed.entries[:5]:

                title = entry.get("title", "")
                summary = entry.get("summary", "")

                fingerprint = make_hash(title + summary)

                # Eğer daha önce işlendiyse atla
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
