import requests
import time

NEWS_SOURCES = [
    "https://newsapi.org/v2/top-headlines?language=en&category=technology",
    "https://newsapi.org/v2/top-headlines?language=en&category=business",
]

topics = []
last_update = 0


def scan_news(api_key: str, limit: int = 10):

    global topics, last_update

    new_topics = []
    seen = set()

    for url in NEWS_SOURCES:

        try:
            r = requests.get(
                f"{url}&apiKey={api_key}",
                timeout=6
            )

            if r.status_code != 200:
                continue

            data = r.json()

            for article in data.get("articles", []):

                title = article.get("title")

                if not title:
                    continue

                title = title.strip()

                if title in seen:
                    continue

                seen.add(title)
                new_topics.append(title)

        except Exception as e:
            print("[RADAR ERROR]", e)

    topics = new_topics[:limit]
    last_update = int(time.time())

    print(f"[RADAR] Detected topics: {len(topics)}")


def get_topics():
    return topics


def get_last_update():
    return last_update


def run(api_key: str, interval: int = 300):

    while True:
        scan_news(api_key)
        time.sleep(interval)

