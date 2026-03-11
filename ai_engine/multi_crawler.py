import feedparser
import requests


RSS_SOURCES = [
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "https://techcrunch.com/feed/"
]


REDDIT_API = "https://www.reddit.com/r/technology/.json"
HN_API = "https://hacker-news.firebaseio.com/v0/topstories.json"


def crawl_rss():

    results = []

    for url in RSS_SOURCES:

        try:

            feed = feedparser.parse(url)

            for entry in feed.entries[:5]:

                results.append({

                    "title": entry.get("title",""),
                    "content": entry.get("summary",""),
                    "source": "rss"

                })

        except Exception as e:
            print("rss error:", e)

    return results


def crawl_reddit():

    results = []

    try:

        r = requests.get(REDDIT_API, headers={"User-Agent":"DynamoHive"})
        data = r.json()

        for post in data["data"]["children"][:5]:

            p = post["data"]

            results.append({

                "title": p.get("title",""),
                "content": p.get("selftext",""),
                "source": "reddit"

            })

    except Exception as e:
        print("reddit error:", e)

    return results


def crawl_hackernews():

    results = []

    try:

        ids = requests.get(HN_API).json()[:5]

        for i in ids:

            item = requests.get(
                f"https://hacker-news.firebaseio.com/v0/item/{i}.json"
            ).json()

            results.append({

                "title": item.get("title",""),
                "content": "",
                "source": "hackernews"

            })

    except Exception as e:
        print("hn error:", e)

    return results


def crawl():

    results = []

    results += crawl_rss()
    results += crawl_reddit()
    results += crawl_hackernews()

    print("multi crawler collected:", len(results))

    return results
