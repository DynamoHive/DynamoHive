import time
import traceback
import hashlib
import threading

from backend.logger import logger
from backend.cache import get_last_data, set_last_data, is_duplicate
from backend.storage import save_signal

from ai_engine.multi_crawler import crawl
from ai_engine.data_pipeline import process_data
from ai_engine.signal_detector import detect_signals
from ai_engine.signal_ranking_engine import merge_ranked_signals
from ai_engine.signal_cluster import cluster_signals

from ai_engine.global_crisis_radar import detect_crisis_signals
from ai_engine.decision_engine import DecisionEngine
from ai_engine.global_intelligence_engine import GlobalIntelligenceEngine


# =====================================================
# BACKFILL ENGINE (SAFE VERSION)
# =====================================================
class BackfillEngine:

    def __init__(self):
        self.last_hash = None
        self.lock = threading.Lock()

    def hash_data(self, data):
        if not data:
            return None

        raw = str(sorted([d.get("title", "") for d in data])).encode("utf-8")
        return hashlib.md5(raw).hexdigest()

    def should_process(self, data):
        new_hash = self.hash_data(data)

        if not new_hash:
            return False

        with self.lock:
            if new_hash == self.last_hash:
                return False

            self.last_hash = new_hash
            return True


# =====================================================
# ORCHESTRATOR
# =====================================================
class Orchestrator:

    def __init__(self):
        self.cycle = 0
        self.decision = DecisionEngine()
        self.intelligence = GlobalIntelligenceEngine()

        self.backfill = BackfillEngine()
        self._lock = threading.Lock()
        self._running = False

    # =====================================================
    # MAIN CYCLE
    # =====================================================
    def run_cycle(self):

        # ---- prevent concurrent cycles (FIXED SAFETY)
        if not self._lock.acquire(blocking=False):
            logger.warning("[ORCHESTRATOR] skipped (cycle in progress)")
            return []

        start = time.time()
        self.cycle += 1

        logger.info(f"[ORCHESTRATOR] cycle {self.cycle} start")

        try:
            # =================================================
            # 1. CRAWL
            # =================================================
            raw = crawl()

            # =================================================
            # 2. BACKFILL SAFETY
            # =================================================
            if not raw:
                raw = get_last_data() or []

            if not raw:
                logger.warning("[ORCHESTRATOR] empty dataset")
                return []

            # =================================================
            # 3. DUPLICATE CYCLE GUARD
            # =================================================
            if not self.backfill.should_process(raw):
                logger.info("[ORCHESTRATOR] duplicate cycle skipped")
                return []

            # =================================================
            # 4. PROCESS DATA
            # =================================================
            raw = process_data(raw)

            if not raw:
                return []

            set_last_data(raw[:100])

            # =================================================
            # 5. CRISIS DETECTION
            # =================================================
            crisis_list = detect_crisis_signals(raw)

            crisis_map = {
                c.get("title", "").lower(): c
                for c in crisis_list if c.get("title")
            }

            # =================================================
            # 6. SIGNAL DETECTION
            # =================================================
            signals = detect_signals(raw)

            if not signals:
                signals = [
                    {"topic": x.get("title", ""), "score": 0.5}
                    for x in raw[:10]
                ]

            signals = cluster_signals(merge_ranked_signals(signals))

            if not signals:
                return []

            # =================================================
            # 7. CRISIS BOOST
            # =================================================
            for s in signals:
                topic = str(s.get("topic", "")).lower()

                if topic in crisis_map:
                    s["score"] = min(float(s.get("score", 0.5)) + 0.3, 1.0)
                    s["urgency"] = crisis_map[topic].get("urgency", "high")

            # =================================================
            # 8. DECISION ENGINE
            # =================================================
            decisions = self.decision.evaluate(signals)

            if not decisions:
                return []

            # =================================================
            # 9. INTELLIGENCE ENGINE
            # =================================================
            intel = self.intelligence.run(decisions)

            if not intel:
                return []

            for i in range(min(len(intel), len(decisions))):
                intel[i]["decision"] = decisions[i]

            # =================================================
            # 10. OUTPUT
            # =================================================
            output = []

            for item in intel:

                topic = (item.get("topic") or "").strip()
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

        except Exception:
            logger.error("[ORCHESTRATOR ERROR]")
            logger.error(traceback.format_exc())
            return []

        finally:
            self._lock.release()
            logger.info(
                f"[ORCHESTRATOR] cycle done in {round(time.time() - start, 2)}s"
            )
