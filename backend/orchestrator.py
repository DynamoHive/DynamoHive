import time

from backend.data_pipeline import start_pipeline
from backend.growth_engine import start_growth
from backend.viral_engine import start_viral_engine

import backend.topic_radar as topic_radar
from backend.analytics_engine import run_analytics
from backend.auto_content_loop import run_content_loop
from backend.feed_engine import generate_feed

from backend.knowledge_ai import run_ai_analysis
from backend.knowledge_graph import update_graph


class DynamoHiveCore:

    def start(self):

        start_pipeline()
        start_growth()
        start_viral_engine()

        while True:

            topic_radar.run()
            run_analytics()

            run_ai_analysis()
            update_graph()

            run_content_loop()
            generate_feed()

            time.sleep(30)
