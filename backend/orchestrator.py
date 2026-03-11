import time

# --- AI ENGINE IMPORTS (Kod-6) ---

from ai_engine.crawler_engine import crawler_engine
from ai_engine.topic_radar import topic_radar
from ai_engine.analytics_engine import analytics_engine
from ai_engine.trend_engine import trend_engine
from ai_engine.signal_detector import signal_detector
from ai_engine.intelligence_engine import intelligence_engine
from ai_engine.growth_engine import growth_engine
from ai_engine.viral_engine import viral_engine

# --- PLATFORM IMPORTS (Kod-5) ---

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

            print("STEP 1: Crawling Internet")

            articles = safe_run(crawler_engine)

            if not articles:
                print("No articles found")
                time.sleep(60)
                continue


            print("STEP 2: Topic Detection")

            topics = safe_run(topic_radar, articles)

            print("Topics:", topics)


            print("STEP 3: Analytics")

            stats = safe_run(analytics_engine, articles)

            print("Stats:", stats)


            print("STEP 4: Trend Analysis")

            trends = safe_run(trend_engine, topics)

            print("Trends:", trends)


            print("STEP 5: Signal Detection")

            signals = safe_run(signal_detector, trends)

            print("Signals:", signals)


            print("STEP 6: Intelligence Generation")

            analysis = safe_run(intelligence_engine, articles)

            if not analysis:
                print("No analysis generated")
                time.sleep(60)
                continue

            print("Analysis items:", len(analysis))


            print("STEP 7: Publishing Content")

            safe_run(publish, analysis)


            print("STEP 8: Growth Engine")

            safe_run(growth_engine)


            print("STEP 9: Viral Engine")

            safe_run(viral_engine)


            print("Cycle Complete")
            print("--------------------------")

            time.sleep(600)
