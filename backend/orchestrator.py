import time
import gc

from backend.logger import logger

from ai_engine.multi_crawler import crawl
from ai_engine.data_pipeline import process_data
from ai_engine.topic_radar import detect_topics
from ai_engine.analytics_engine import analyse
from ai_engine.signal_detector import detect_signals
from ai_engine.global_intelligence_engine import generate_intelligence
from ai_engine.knowledge_graph import update_graph
from ai_engine.topic_learning_engine import learn_topics
from ai_engine.trend_scoring_engine import is_trending

from ai_engine.signal_ranking_engine import rank_signals
from ai_engine.memory_pattern_engine import MemoryPatternEngine

# newsroom layer
from backend.newsroom.story_engine import build_story
from backend.newsroom.editorial_engine import apply_editorial
from backend.newsroom.article_engine import generate_article
from backend.newsroom.publish_engine import publish_article


CYCLE_INTERVAL = 600
ERROR_SLEEP = 30

memory_engine = MemoryPatternEngine()


def run_cycle():

    start_time = time.time()

    logger.info("DynamoHive cycle started")

    try:

        # 1️⃣ Crawl
        raw_data = crawl() or []

        if not raw_data:
            logger.warning("Crawler returned no data")
            return

        # 2️⃣ Pipeline processing
        processed = process_data(raw_data) or []

        if not processed:
            logger.warning("Pipeline produced no usable data")
            return

        # 3️⃣ Topic detection
        topics = detect_topics(processed) or []

        if not topics:
            logger.warning("No topics detected")
            return

        # 4️⃣ Analytics
        analytics = analyse(topics) or {}

        # 5️⃣ Signal detection
        signals = detect_signals(analytics) or []

        if not signals:
            logger.info("No signals detected")
            return

        # 6️⃣ Ranking
        signals = rank_signals(signals)

        # 7️⃣ Memory filtering
        new_signals = []

        for s in signals:

            if not memory_engine.seen_before(s):

                memory_engine.store(s)

                new_signals.append(s)

        if not new_signals:
            logger.info("All signals filtered by memory engine")
            return

        # 8️⃣ Intelligence generation
        intelligence = generate_intelligence(new_signals)

        if not intelligence:
            logger.info("No intelligence generated")
            return

        # 9️⃣ Knowledge graph update
        try:
            update_graph(intelligence)
        except Exception as e:
            logger.warning(f"Knowledge graph update failed: {e}")

        # 10️⃣ Topic learning
        try:
            learn_topics(intelligence)
        except Exception as e:
            logger.warning(f"Topic learning failed: {e}")

        # 11️⃣ Trend filter
        if not is_trending(intelligence):
            logger.info("Topic skipped (not trending)")
            return

        # 12️⃣ Newsroom pipeline
        story = build_story(intelligence)

        story = apply_editorial(story)

        article = generate_article(story)

        publish_article(article)

        logger.info("Intelligence article published")

    except Exception as e:

        logger.error(f"Cycle error: {e}")

    finally:

        gc.collect()

        elapsed = round(time.time() - start_time, 2)

        logger.info(f"Cycle finished in {elapsed}s")


def start():

    logger.info("DynamoHive system started")

    while True:

        try:

            run_cycle()

            time.sleep(CYCLE_INTERVAL)

        except Exception as e:

            logger.error(f"System error: {e}")

            time.sleep(ERROR_SLEEP)

          
