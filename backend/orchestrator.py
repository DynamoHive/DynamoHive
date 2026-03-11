import time

from ai_engine.crawler_engine import crawler_engine
from ai_engine.topic_radar import topic_radar
from ai_engine.intelligence_engine import intelligence_engine

from backend.feed_engine import publish


def safe_run(fn, *args):

    try:
        return fn(*args)

    except Exception as e:
        print("Engine error:", e)
        return None


class DynamoHiveCore:

    def start(self):

        print("DynamoHive core started")

        while True:

            print("Running crawler")

            articles = safe_run(crawler_engine)

            if not articles:
                time.sleep(60)
                continue

            print("Detecting topics")

            topics = safe_run(topic_radar, articles)

            print("Generating analysis")

            analysis = safe_run(intelligence_engine, articles)

            if analysis:

                print("Publishing analysis")

                safe_run(publish, analysis)

            print("Cycle complete")

            time.sleep(600)
