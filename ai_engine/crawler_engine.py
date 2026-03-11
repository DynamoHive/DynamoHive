import feedparser
from ai_engine.sources import RSS_SOURCES


def crawl():

    results = []

    for url in RSS_SOURCES:

        try:

            feed = feedparser.parse(url)

            for entry in feed.entries[:5]:

                results.append({

                    "title": entry.get("title",""),
                    "content": entry.get("summary",""),
                    "source": url

                })

        except Exception as e:

            print("crawler error:", e)

    print("crawler collected:", len(results))

    return results
