import time
import gc
from concurrent.futures import ThreadPoolExecutor

from backend.logger import logger

from backend.ai_engine.multi_crawler import crawl
from backend.ai_engine.data_pipeline import process_data
from backend.ai_engine.topic_radar import detect_topics
from backend.ai_engine.analytics_engine import analyse
from backend.ai_engine.signal_detector import detect_signals
from backend.ai_engine.global_intelligence_engine import generate_intelligence
from backend.ai_engine.knowledge_graph import update_graph
from backend.ai_engine.topic_learning_engine import learn_topics
from backend.ai_engine.trend_scoring_engine import is_trending
from backend.ai_engine.signal_ranking_engine import rank_signals
from backend.ai_engine.memory_pattern_engine import MemoryPatternEngine

from backend.newsroom.story_engine import build_story
from backend.newsroom.editorial_engine import apply_editorial
from backend.newsroom.article_engine import generate_article
from backend.newsroom.publish_engine import publish_article


CYCLE_INTERVAL = 30
ERROR_SLEEP = 30
MAX_WORKERS = 4

memory_engine = MemoryPatternEngine()


def parallel_crawl():

    try:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future = executor.submit(crawl)
            data = future.result()

        return data or []

    except Exception as e:
        logger.error(f"Crawl failed: {e}")
        return []


def newsroom_pipeline(intel):

    try:

        if not is_trending(intel):
            return False

        story = build_story(intel)

        story = apply_editorial(story)

        article = generate_article(story)

        if article:
            publish_article(article)

        return True

    except Exception as e:
        logger.warning(f"Newsroom error: {e}")
        return False


def run_cycle():

    start_time = time.time()

    logger.info("DynamoHive cycle started")

    try:

        raw_data = parallel_crawl()

        if not raw_data:
            logger.warning("No crawl data")
            return

        processed = process_data(raw_data) or []

        if not processed:
            logger.warning("No processed data")
            return

        topics = detect_topics(processed) or []

        if not topics:
            logger.warning("No topics detected")
            return

        analytics = analyse(topics) or {}

        signals = detect_signals(analytics) or []

        if not signals:
            logger.info("No signals detected")
            return

        signals = rank_signals(signals)

        new_signals = []

        for s in signals:

            if not memory_engine.seen_before(s):
                memory_engine.store(s)
                new_signals.append(s)

        if not new_signals:
            logger.info("All signals filtered")
            return

        intelligence = generate_intelligence(new_signals)

        if not intelligence:
            logger.info("No intelligence generated")
            return

        if not isinstance(intelligence, list):
            intelligence = [intelligence]

        try:
            update_graph(intelligence)
        except Exception as e:
            logger.warning(f"Graph update failed: {e}")

        try:
            learn_topics(intelligence)
        except Exception as e:
            logger.warning(f"Topic learning failed: {e}")

        published = 0

        for intel in intelligence:

            if newsroom_pipeline(intel):
                published += 1

        logger.info(f"Articles published: {published}")

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
