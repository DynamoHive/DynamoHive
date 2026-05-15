import time
import traceback
import hashlib

from backend.logger import logger
from backend.storage import save_signal

from ai_engine.multi_crawler import crawl
from ai_engine.data_pipeline import process_data
from ai_engine.signal_detector import detect_signals
from ai_engine.signal_ranking_engine import merge_ranked_signals
from ai_engine.signal_cluster import cluster_signals

from ai_engine.global_intelligence_engine import GlobalIntelligenceEngine
from ai_engine.decision_engine import DecisionEngine
from ai_engine.global_crisis_radar import detect_crisis_signals


LAST_DATA = []
duplicate_cache = {}


def is_duplicate(topic: str) -> bool:
    try:
        bucket = int(time.time() / 300)
        key = hashlib.md5((str(topic).lower() + str(bucket)).encode()).hexdigest()
    except Exception:
        return False

    now = time.time()

    if key in duplicate_cache and now - duplicate_cache[key] < 300:
        return True

    duplicate_cache[key] = now

    if len(duplicate_cache) > 10000:
        duplicate_cache.clear()

    return False


class Orchestrator:

    def __init__(self):
        self.cycle = 0
        self.intelligence = GlobalIntelligenceEngine()
        self.decision = DecisionEngine()

    def run_cycle(self):

        start = time.time()
        self.cycle += 1

        logger.info(f"[ORCHESTRATOR] Cycle {self.cycle} started")

        try:
            raw = crawl()

            if not raw:
                raw = LAST_DATA or []

            raw = process_data(raw)

            if not raw:
                return []

            LAST_DATA.clear()
            LAST_DATA.extend(raw[:100])

            crisis_signals = detect_crisis_signals(raw)

            crisis_map = {
                str(c.get("title", "")).lower(): c
                for c in crisis_signals
            }

            signals = detect_signals(raw)

            if not signals:
                signals = [
                    {"topic": x.get("title", ""), "score": 0.5}
                    for x in raw[:10]
                ]

            signals = merge_ranked_signals(signals or [])
            signals = cluster_signals(signals or [])

            if not signals:
                return []

            for s in signals:
                topic = str(s.get("topic", "")).lower()

                if topic in crisis_map:
                    s["urgency"] = crisis_map[topic].get("urgency", "high")
                    s["score"] = min(float(s.get("score", 0.5)) + 0.3, 1.0)

            decisions = self.decision.evaluate(signals)

            if not decisions:
                return []

            intel = self.intelligence.run(decisions)

            if not intel:
                return []

            for i, item in enumerate(intel):
                if i < len(decisions):
                    item["decision"] = decisions[i]

            output = []

            for item in intel:

                topic = str(item.get("topic", "")).strip()
                if not topic:
                    continue

                decision = item.get("decision", {})

                if not decision.get("publish", True):
                    continue

                if is_duplicate(topic):
                    continue

                narrative = item.get("narrative") or {}

                payload = {
                    "title": narrative.get("title") or topic[:80],
                    "topic": topic,
                    "content": narrative.get("content") or topic,
                    "priority": float(decision.get("priority", 0.5)),
                    "published": True,
                    "timestamp": int(time.time())
                }

                save_signal(payload)
                output.append(payload)

                logger.info(f"[GENERATED] {topic}")

            return output

        except Exception as e:
            traceback.print_exc()
            logger.error(f"[ORCHESTRATOR ERROR] {str(e)}")
            return []

        finally:
            logger.info(f"[ORCHESTRATOR] Cycle finished in {round(time.time() - start, 2)}s")
