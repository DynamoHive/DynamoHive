import time

from ai_engine.crawler_engine import crawl
from ai_engine.topic_radar import detect_topics
from ai_engine.analytics_engine import analyse
from ai_engine.signal_detector import detect_signals
from ai_engine.intelligence_engine import generate_intelligence
from ai_engine.auto_content_loop import generate_content

from backend.feed_engine import publish


def run_cycle():

    data = crawl()

    topics = detect_topics(data)

    analysis = analyse(data)

    signals = detect_signals(analysis)

    intelligence = generate_intelligence(signals)

    post = generate_content(intelligence)

    publish(post)


def start():

    while True:

        try:

            run_cycle()

        except Exception as e:

            print("Pipeline error:", e)

        time.sleep(600)
