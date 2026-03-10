import requests

NEWS_SOURCES = [
    "https://newsapi.org/v2/top-headlines?language=en&category=technology",
    "https://newsapi.org/v2/top-headlines?language=en&category=business",
]

topics = []


def scan_news():

    global topics

    new_topics = []

    for url in NEWS_SOURCES:
        try:
            r = requests.get(url, timeout=5)
            data = r.json()

            for article in data.get("articles", []):
                title = article.get("title")
                if title:
                    new_topics.append(title)

        except Exception as e:
            print("Radar error:", e)

    topics = new_topics[:10]

    print("Detected topics:", topics)


def run():
    scan_news()


