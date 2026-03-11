import requests
import feedparser


SOURCES = [

    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "https://www.theverge.com/rss/index.xml"

]


def crawl():

    results = []

    for url in SOURCES:

        try:

            feed = feedparser.parse(url)

            for entry in feed.entries[:5]:

                title = entry.get("title", "")
                summary = entry.get("summary", "")

                results.append({

                    "title": title,
                    "content": summary,
                    "source": url

                })

        except Exception as e:

            print("crawler error:", e)

    print("crawler collected:", len(results))

    return results
