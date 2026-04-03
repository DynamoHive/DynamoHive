import time
import traceback
import hashlib

from backend.logger import logger

# ENGINE IMPORTS
from ai_engine.multi_crawler import crawl
from ai_engine.data_pipeline import process_data
import ai_engine.signal_detector as signal_module

from ai_engine.global_intelligence_engine import GlobalIntelligenceEngine
from ai_engine.predictive_engine import update_trends  # 🔥 NEW

from backend.events import register_event, detect_event_spikes
from backend.user_profile_engine import get_user_profile, compute_final_score

from ai_engine.narrative_engine import generate_narrative

from backend.storage import save_post, get_posts
from backend.distribution_engine import distribute

from ai_engine.anomaly_engine import detect_anomalies
from ai_engine.dominance_engine import compute_dominance

from ai_engine.memory_pattern_engine import MemoryPatternEngine
from ai_engine.content_filter import is_low_quality
from ai_engine.vector_memory import search_similar, store_vector

# 🔥 GLOBAL DATA FIX
GLOBAL_DATA = []

intel_engine = GlobalIntelligenceEngine()

duplicate_cache = {}


# -------------------------
# DUPLICATE
# -------------------------
def is_duplicate_local(topic):
    try:
        topic = str(topic).lower().strip()
        h = hashlib.md5(topic.encode()).hexdigest()
    except:
        return False

    now = time.time()

    if h in duplicate_cache:
        if now - duplicate_cache[h] < 7200:
            return True

    duplicate_cache[h] = now
    return False


# -------------------------
# 🔥 SIGNAL MERGE (FIX)
# -------------------------
def merge_signals(signals):

    merged = {}

    for s in signals:
        topic = s["topic"]

        if topic not in merged:
            merged[topic] = s
        else:
            merged[topic]["score"] += s["score"]

    return list(merged.values())


# -------------------------
# ORCHESTRATOR
# -------------------------
class Orchestrator:

    def __init__(self):
        self.cycle_count = 0
        self.last_run = None
        self.last_duration = 0
        self.last_signal_count = 0
        self.last_event_count = 0
        self.last_anomalies = []
        self.last_dominance = []

        self.pattern_memory = MemoryPatternEngine()

    # -------------------------
    # MAIN LOOP
    # -------------------------
    def run_cycle(self):

        start = time.time()
        self.cycle_count += 1
        self.last_run = start

        logger.info(f"[ORCHESTRATOR] Cycle {self.cycle_count} started")

        try:

            # -------------------------
            # DATA
            # -------------------------
            raw_data = crawl()

            if not raw_data:
                raw_data = get_posts() or [{"text": "bootstrap signal"}]

            raw_data = process_data(raw_data)

            # 🔥 GLOBAL DATA FILL
            GLOBAL_DATA.clear()
            GLOBAL_DATA.extend(raw_data[:100])

            # -------------------------
            # SIGNAL
            # -------------------------
            signals = signal_module.detect_signals(raw_data)

            if not signals:
                signals = []
                for item in raw_data[:20]:
                    text = item.get("title") or item.get("text")
                    if text:
                        signals.append({
                            "topic": text,
                            "score": 1.0
                        })

            # 🔥 MERGE FIX
            signals = merge_signals(signals)

            # -------------------------
            # NORMALIZE
            # -------------------------
            normalized = []
            for s in signals:

                topic = (
                    s.get("topic")
                    or s.get("text")
                    or s.get("title")
                    or ""
                )

                topic = str(topic).strip()

                if len(topic) < 5:
                    continue

                normalized.append({
                    "topic": topic,
                    "score": float(s.get("score", 1.0))
                })

            signals = normalized
            self.last_signal_count = len(signals)

            # -------------------------
            # EVENTS
            # -------------------------
            for s in signals:
                register_event(s["topic"])

            events = detect_event_spikes()
            self.last_event_count = len(events)

            # -------------------------
            # PERSONALIZATION
            # -------------------------
            profile = get_user_profile("global_user")

            for s in signals:
                try:
                    s["score"] = compute_final_score(s, profile)
                except:
                    pass

            # -------------------------
            # ANOMALY + DOMINANCE
            # -------------------------
            try:
                self.last_anomalies = detect_anomalies(signals, events)
            except Exception as e:
                logger.warning(f"[ANOMALY ERROR] {e}")
                self.last_anomalies = []

            try:
                self.last_dominance = compute_dominance(signals)
            except Exception as e:
                logger.warning(f"[DOMINANCE ERROR] {e}")
                self.last_dominance = []

            # -------------------------
            # INTELLIGENCE
            # -------------------------
            intelligence = signals

            try:
                intelligence = intel_engine.process(intelligence)
            except Exception as e:
                logger.warning(f"[INTEL ERROR] {e}")

            # 🔥 PREDICTIVE UPDATE
            try:
                update_trends(intelligence)
            except Exception as e:
                logger.warning(f"[PREDICT ERROR] {e}")

            # -------------------------
            # CONTENT
            # -------------------------
            self._generate_content(intelligence)

        except Exception:
            traceback.print_exc()

        finally:
            duration = round(time.time() - start, 2)
            self.last_duration = duration
            logger.info(f"[ORCHESTRATOR] Cycle finished in {duration}s")

    # -------------------------
    # CONTENT
    # -------------------------
    def _generate_content(self, intelligence):

        for intel in intelligence:

            topic = str(intel.get("topic", "")).strip()

            if not topic or len(topic) < 5:
                continue

            if is_duplicate_local(topic):
                continue

            if self.pattern_memory.seen_before(topic):
                continue

            similar = search_similar(topic)
            if similar:
                try:
                    if similar[0]["score"] > 0.92:
                        continue
                except:
                    pass

            content = generate_narrative(intel)

            if not content:
                continue

            title = content.get("title")
            body = content.get("content")

            if not title or not body:
                continue

            if is_low_quality(body):
                continue

            if len(body) < 80:
                continue

            try:
                save_post(title, body)
            except Exception:
                logger.warning("[SAVE ERROR]")
                continue

            self.pattern_memory.store(topic)

            try:
                store_vector(content)
            except Exception:
                logger.warning("[VECTOR ERROR]")

            try:
                distribute(content)
            except Exception:
                logger.warning("[DISTRIBUTION ERROR]")

            logger.info(f"[ORCHESTRATOR] GENERATED: {topic}")

    # -------------------------
    # STATUS
    # -------------------------
    def get_status(self):
        return {
            "cycle_count": self.cycle_count,
            "last_run": self.last_run,
            "last_duration": self.last_duration,
            "last_signal_count": self.last_signal_count,
            "last_event_count": self.last_event_count,
            "anomalies": self.last_anomalies,
            "dominance": self.last_dominance[:5]
        }
