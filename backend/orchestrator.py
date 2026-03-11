import time

from ai_engine.crawler_engine import crawl
from ai_engine.topic_radar import detect_topics
from ai_engine.analytics_engine import analyse
from ai_engine.signal_detector import detect_signals
from ai_engine.intelligence_engine import generate_intelligence
from ai_engine.knowledge_graph import update_graph
from ai_engine.vector_memory import store_vector
from ai_engine.auto_content_loop import generate_content

from backend.feed_engine import publish


CYCLE_TIME = 600


def run_cycle():

    print("DynamoHive cycle start")

    # 1 INTERNET CRAWL
    data = crawl()

    if not data:
        print("crawler returned no data")
        return

    # 2 TOPIC DETECTION
    topics = detect_topics(data)

    # 3 ANALYSIS
    analysis = analyse(data)

    # 4 SIGNAL DETECTION
    signals = detect_signals(analysis)

    # 5 INTELLIGENCE
    intelligence = generate_intelligence(signals)

    # 6 KNOWLEDGE GRAPH UPDATE
    update_graph(intelligence)

    # 7 VECTOR MEMORY
    store_vector(intelligence)

    # 8 CONTENT GENERATION
    post = generate_content(intelligence)

    if not post:
        print("no content generated")
        return

    # 9 PUBLISH
    publish(post)

    print("cycle complete")


def start():

    print("DynamoHive orchestrator started")

    while True:

        try:

            run_cycle()

        except Exception as e:

            print("orchestrator error:", e)

        time.sleep(CYCLE_TIME)
