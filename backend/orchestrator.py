import time
import traceback
import hashlib

from backend.logger import logger

from ai_engine.multi_crawler import crawl
from ai_engine.data_pipeline import process_data
from ai_engine.signal_detector import detect_signals
from ai_engine.signal_ranking_engine import merge_ranked_signals

from ai_engine.global_intelligence_engine import GlobalIntelligenceEngine
from ai_engine.decision_engine import DecisionEngine

from backend.storage import save_post


LAST_DATA = []
duplicate_cache = {}


def is_duplicate(topic):
    h = hashlib.md5(str(topic).lower().encode()).hexdigest()
    now = time.time()

    if h in duplicate_cache and now - duplicate_cache[h] < 3600:
        return True

    duplicate_cache[h] = now
    return False


class Orchestrator:

    def __init__(self):
        self.cycle = 0
        self.intelligence = GlobalIntelligenceEngine()
        self.decision = DecisionEngine()

    def run_cycle(self):

        self.cycle += 1
        start = time.time()

        try:
            raw = crawl() or LAST_DATA or [{"title": "fallback signal"}]

            raw = process_data(raw)
            LAST_DATA.clear()
            LAST_DATA.extend(raw[:100])

            signals = detect_signals(raw) or []

            signals = merge_ranked_signals(signals)

            # 🔥 CORE INTELLIGENCE
            intel_items = self.intelligence.run(signals)

            # 🔥 DECISION
            decisions = self.decision.evaluate(intel_items)

            # 🔥 GENERATION
            for item in decisions:

                if not item.get("decision", {}).get("publish"):
                    continue

                topic = item.get("topic", "")
                if len(topic) < 5:
                    continue

                if is_duplicate(topic):
                    continue

                narrative = item.get("narrative")

                if not narrative:
                    continue

                title = narrative.get("title")
                content = narrative.get("content")

                if not title or not content:
                    continue

                save_post(title, content)

                logger.info(f"[GENERATED] {topic}")

        except Exception:
            traceback.print_exc()

        finally:
            logger.info(f"[CYCLE DONE] {round(time.time()-start,2)}s")
