import feedparser

RSS_FEEDS = [
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "https://www.reuters.com/technology/rss"
]

def crawler_engine():

    articles = []

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:5]:
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.summary
            })

    return articles
