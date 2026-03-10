import time

from backend.data_pipeline import start_pipeline
from backend.growth_engine import start_growth
from backend.viral_engine import start_viral_engine


class DynamoHiveCore:

    def start(self):

        start_pipeline()
        start_growth()
        start_viral_engine()

        while True:
            time.sleep(30)
