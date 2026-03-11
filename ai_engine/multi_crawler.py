import feedparser
import requests
from concurrent.futures import ThreadPoolExecutor

from ai_engine.source_manager import get_rss_sources


REDDIT_API = "https://www.reddit.com/r/technology/.json"
HN_API = "https://hacker-news.firebaseio.com/v0/topstories.json"


HEADERS = {
    "User-Agent": "DynamoHive"
}


# basit duplicate filtresi
seen_titles = set()


def add_item(results, title, content, source):

    if not title:
        return

    if title in seen_titles:
        return

    seen_titles.add(title)

    results.append({
        "title": title,
        "content": content,
        "source": source
    })


def crawl_single_rss(url):

    items = []

    try:

        feed = feedparser.parse(url)

        for entry in feed.entries[:10]:

            title = entry.get("title", "")
            summary = entry.get("summary", "")

            items.append((title, summary, "rss"))

    except Exception as e:
        print("rss error:", e)

    return items


def crawl_rss():

    results = []
    sources = get_rss_sources()

    with ThreadPoolExecutor(max_workers=5) as executor:

        feeds = list(executor.map(crawl_single_rss, sources))

    for feed_items in feeds:

        for title, summary, source in feed_items:

            add_item(results, title, summary, source)

    return results


def crawl_reddit():

    results = []

    try:

        r = requests.get(REDDIT_API, headers=HEADERS, timeout=10)

        data = r.json()

        for post in data["data"]["children"][:10]:

            p = post["data"]

            title = p.get("title", "")
            text = p.get("selftext", "")

            add_item(results, title, text, "reddit")

    except Exception as e:
        print("reddit error:", e)

    return results


def crawl_hackernews():

    results = []

    try:

        ids = requests.get(HN_API, timeout=10).json()[:10]

        for i in ids:

            item = requests.get(
                f"https://hacker-news.firebaseio.com/v0/item/{i}.json",
                timeout=10
            ).json()

            title = item.get("title", "")

            add_item(results, title, "", "hackernews")

    except Exception as e:
        print("hn error:", e)

    return results


def crawl():

    results = []

    results.extend(crawl_rss())
    results.extend(crawl_reddit())
    results.extend(crawl_hackernews())

    print("multi crawler collected:", len(results))

    return results
