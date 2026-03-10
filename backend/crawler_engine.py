import requests

SOURCES = [
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://feeds.bbci.co.uk/news/world/rss.xml",
]

articles = []


def crawl():

    global articles

    results = []

    for url in SOURCES:

        try:
            r = requests.get(url, timeout=5)
            text = r.text

            results.append({
                "source": url,
                "data": text[:500]
            })

        except Exception as e:
            print("Crawler error:", e)

    articles = results

    print("Crawler collected:", len(articles))


def run():
    crawl()
