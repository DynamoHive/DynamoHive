import time
import traceback
import hashlib

from backend.logger import logger

# ENGINE IMPORTS
from ai_engine.multi_crawler import crawl
from ai_engine.data_pipeline import process_data
import ai_engine.signal_detector as signal_module

from backend.events import register_event, detect_event_spikes
from backend.user_profile_engine import get_user_profile, compute_final_score

from ai_engine.global_intelligence_engine import GlobalIntelligenceEngine
from ai_engine.narrative_engine import generate_narrative

from backend.storage import save_post, get_posts
from backend.distribution_engine import distribute

from ai_engine.anomaly_engine import detect_anomalies
from ai_engine.dominance_engine import compute_dominance


intel_engine = GlobalIntelligenceEngine()

# -------------------------
# 🔥 DUPLICATE CACHE (GÜÇLENDİRİLDİ)
# -------------------------
duplicate_cache = {}

def is_duplicate_local(topic):

    try:
        topic = str(topic).lower().strip()
        h = hashlib.md5(topic.encode()).hexdigest()
    except:
        return False

    now = time.time()

    # 🔥 2 SAAT BLOK (daha güçlü)
    if h in duplicate_cache:
        if now - duplicate_cache[h] < 7200:
            return True

    duplicate_cache[h] = now
    return False


class Orchestrator:

    def __init__(self):
        self.cycle_count = 0
        self.last_run = None
        self.last_duration = 0
        self.last_signal_count = 0
        self.last_event_count = 0
        self.last_anomalies = []
        self.last_dominance = []

    # -------------------------
    # 🚀 MAIN LOOP
    # -------------------------
    def run_cycle(self):

        start = time.time()
        self.cycle_count += 1
        self.last_run = start

        logger.info(f"[ORCHESTRATOR] Cycle {self.cycle_count} started")

        try:

            # -------------------------
            # 1. DATA
            # -------------------------
            raw_data = crawl()

            if not raw_data:
                raw_data = get_posts() or [{"text": "bootstrap"}]

            raw_data = process_data(raw_data)

            # -------------------------
            # 2. SIGNAL
            # -------------------------
            signals = signal_module.detect_signals(raw_data)

            # 🔥 fallback → sistem kör kalmasın
            if not signals or len(signals) <= 2:
                signals = []

                for item in raw_data:
                    text = item.get("title") or item.get("text")
                    if not text:
                        continue

                    signals.append({
                        "text": text,
                        "score": 1.0
                    })

            self.last_signal_count = len(signals)

            # -------------------------
            # 3. EVENTS
            # -------------------------
            for s in signals:
                topic = s.get("text") or s.get("topic")
                if topic:
                    register_event(topic)

            events = detect_event_spikes()
            self.last_event_count = len(events)

            # -------------------------
            # 4. PERSONALIZATION
            # -------------------------
            profile = get_user_profile("global_user")

            for s in signals:
                topic = (
                    s.get("text")
                    or s.get("topic")
                    or s.get("title")
                    or "unknown"
                )

                base_score = s.get("score", 0)

                try:
                    s["score"] = compute_final_score(
                        {"topic": topic, "score": base_score},
                        profile
                    )
                except:
                    pass

                s["text"] = topic

            # -------------------------
            # 5. ANOMALY + DOMINANCE
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
            # 6. INTELLIGENCE
            # -------------------------
            intelligence = self._build_intelligence(signals)

            try:
                intelligence = intel_engine.process(intelligence)
            except Exception as e:
                logger.warning(f"[INTEL ERROR] {e}")

            # -------------------------
            # 7. CONTENT
            # -------------------------
            self._generate_content(intelligence)

        except Exception:
            traceback.print_exc()

        finally:
            duration = round(time.time() - start, 2)
            self.last_duration = duration

            logger.info(f"[ORCHESTRATOR] Cycle finished in {duration}s")

    # -------------------------
    # 🧠 INTELLIGENCE BUILDER
    # -------------------------
    def _build_intelligence(self, signals):

        intelligence = []

        for s in signals:
            topic = s.get("text") or "unknown"

            intelligence.append({
                "topic": topic,
                "summary": f"{topic} shows emerging structural signals in global systems.",
                "trend": "surging" if s.get("score", 0) > 3 else "rising"
            })

        return intelligence

    # -------------------------
    # 📰 CONTENT ENGINE
    # -------------------------
    def _generate_content(self, intelligence):

        for intel in intelligence:

            topic = intel.get("topic") or "unknown"

            # 🔥 CRITICAL → DUPLICATE KES
            if is_duplicate_local(topic):
                continue

            try:
                content = generate_narrative(intel)
            except Exception:
                continue

            if not content:
                continue

            title = content.get("title") or topic
            body = content.get("content") or "No content"

            try:
                save_post(title, body)
            except Exception:
                logger.warning("[SAVE ERROR]")
                continue

            try:
                distribute(content)
            except Exception:
                logger.warning("[DISTRIBUTION ERROR]")

            logger.info(f"[ORCHESTRATOR] GENERATED: {topic}")

    # -------------------------
    # 📊 STATUS
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
