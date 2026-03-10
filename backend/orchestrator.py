import time


def safe_run(fn):
    try:
        fn()
    except Exception as e:
        print("Engine error:", e)


# ---- AI MODULES ----

def crawler_engine():
    print("Crawler engine running")


def topic_radar():
    print("Topic radar running")


def analytics_engine():
    print("Analytics engine running")


def trend_engine():
    print("Trend engine running")


def signal_detector():
    print("Signal detector running")


def intelligence_engine():
    print("Intelligence engine running")


def growth_engine():
    print("Growth engine running")


def viral_engine():
    print("Viral engine running")


# ---- CORE LOOP ----

class DynamoHiveCore:

    def start(self):

        print("DynamoHive core started")

        while True:

            safe_run(crawler_engine)
            safe_run(topic_radar)
            safe_run(analytics_engine)
            safe_run(trend_engine)
            safe_run(signal_detector)
            safe_run(intelligence_engine)
            safe_run(growth_engine)
            safe_run(viral_engine)

            time.sleep(5)
