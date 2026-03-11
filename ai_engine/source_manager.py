# DynamoHive source manager
# tüm crawler kaynakları burada tutulur


RSS_SOURCES = [

    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://www.wired.com/feed/rss",
    "https://arstechnica.com/feed/",
    "https://www.engadget.com/rss.xml",
    "https://feeds.feedburner.com/venturebeat/SZYF",
    "https://www.cnet.com/rss/news/",
    "https://www.zdnet.com/news/rss.xml"

]


REDDIT_SOURCES = [

    "https://www.reddit.com/r/technology/.json",
    "https://www.reddit.com/r/artificial/.json",
    "https://www.reddit.com/r/MachineLearning/.json"

]


HN_API = "https://hacker-news.firebaseio.com/v0/topstories.json"


def get_rss_sources():

    return RSS_SOURCES


def get_reddit_sources():

    return REDDIT_SOURCES


def get_hn_api():

    return HN_API
