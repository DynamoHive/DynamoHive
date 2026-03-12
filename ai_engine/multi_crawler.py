import feedparser
import requests

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


def crawl():

    results = []

    for url in RSS_SOURCES:

        try:

            feed = feedparser.parse(url)

            for entry in feed.entries[:5]:

                results.append({

                    "title": entry.get("title", ""),

                    "content": entry.get(
                        "summary",
                        entry.get("description", "")
                    ),

                    "source": url
                })

        except Exception as e:

            print("rss error:", e)

    print("crawler collected:", len(results))

    return results
