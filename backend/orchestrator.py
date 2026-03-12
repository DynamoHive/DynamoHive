import time
from backend.logger import logger

# --- AI ENGINE IMPORTS ---

from ai_engine.multi_crawler import crawl
from ai_engine.data_pipeline import process_data
from ai_engine.topic_radar import detect_topics
from ai_engine.analytics_engine import analyse
from ai_engine.signal_detector import detect_signals
from ai_engine.intelligence_engine import generate_intelligence
from ai_engine.auto_content_loop import generate_content

from ai_engine.knowledge_graph import update_graph
from ai_engine.topic_learning_engine import learn_topics


LOOP_INTERVAL = 600  # seconds


def dynamo_cycle():

    logger.info("DynamoHive cycle started")

    # 1️⃣ Crawl sources
    raw_data = crawl()

    # 2️⃣ Process data
    structured_data = process_data(raw_data)

    # 3️⃣ Detect topics
    topics = detect_topics(structured_data)

    # 4️⃣ Analytics
    analytics = analyse(topics)

    # 5️⃣ Detect signals
    signals = detect_signals(analytics)

    # 6️⃣ Intelligence layer
    intelligence = generate_intelligence(signals)

    # 7️⃣ Update knowledge graph
    update_graph(intelligence)

    # 8️⃣ Topic learning
    learn_topics(intelligence)

    # 9️⃣ Generate content
    content = generate_content(intelligence)

    logger.info("Cycle finished")

    return content


def start_dynamohive():

    logger.info("DynamoHive system booting")

    while True:

        try:

            dynamo_cycle()

        except Exception as e:

            logger.error(f"DynamoHive error: {e}")

        time.sleep(LOOP_INTERVAL)


if __name__ == "__main__":
    start_dynamohive()
