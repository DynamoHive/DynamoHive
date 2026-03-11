import time

from ai_engine.crawler_engine import crawler_engine
from ai_engine.topic_radar import topic_radar
from ai_engine.intelligence_engine import intelligence_engine

from backend.feed_engine import publish


def safe_run(fn, *args):

    try:
        return fn(*args)

    except Exception as e:
        print("ENGINE ERROR:", fn.__name__, e)
        return None


class DynamoHiveCore:

    def start(self):

        print("DynamoHive Core Started")

        while True:

            print("Step 1: Crawling")

            articles = safe_run(crawler_engine)

            if not articles:
                time.sleep(60)
                continue

            print("Step 2: Topic Detection")

            topics = safe_run(topic_radar, articles)

            print("Topics:", topics)

            print("Step 3: Intelligence Analysis")

            analysis = safe_run(intelligence_engine, articles)

            if analysis:

                print("Step 4: Publishing")

                safe_run(publish, analysis)

            print("Cycle Complete")

            time.sleep(600)
