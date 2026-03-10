from backend.orchestrator import DynamoHiveCorefrom backend.analytics_engine import run_analytics
from backend.topic_radar import scan_topics
from backend.auto_content_loop import run_content_loop
from backend.feed_engine import generate_feed


class DynamoHiveCore:

    def start(self):
        print("DynamoHive Orchestrator starting")

        # başlangıç motorları
        start_pipeline()
        start_growth()
        start_viral_engine()

        self.run_loop()

    def run_loop(self):
        while True:

            scan_topics()
            run_analytics()
            run_content_loop()
            generate_feed()

            time.sleep(30)
