import time
import traceback
import hashlib

from backend.logger import logger

# -------------------------
# SAFE IMPORTS
# -------------------------

try:
    from ai_engine.multi_crawler import crawl
except:
    def crawl(): return []

try:
    from ai_engine.data_pipeline import process_data
except:
    def process_data(x): return x

try:
    from ai_engine.signal_detector import detect_signals
except:
    def detect_signals(x): return []

try:
    from ai_engine.ranking_engine import merge_ranked_signals
except:
    def merge_ranked_signals(x): return x

try:
    from ai_engine.intelligence_layer import enrich_intelligence
except:
    def enrich_intelligence(x): return x

try:
    from ai_engine.importance_engine import compute_importance
except:
    def compute_importance(x): return x

try:
    from ai_engine.decision_engine import run_decision_pipeline
except:
    def run_decision_pipeline(x): return x

try:
    from backend.storage import save_post
except:
    def save_post(*a, **k): pass


# -------------------------
# GLOBALS
# -------------------------

LAST_DATA = []
duplicate_cache = {}


def is_duplicate(topic):
    try:
        h = hashlib.md5(str(topic).lower().encode()).hexdigest()
    except:
        return False

    now = time.time()

    if h in duplicate_cache and now - duplicate_cache[h] < 3600:
        return True

    duplicate_cache[h] = now
    return False


def safe_generate(intel):
    topic = str(intel.get("topic", ""))

    return {
        "title": topic[:80],
        "content": f"{topic} is emerging as a significant global signal."
    }


def force_signals(raw):
    out = []

    for item in raw[:5]:
        text = item.get("title") or item.get("text")

        if text:
            out.append({
                "topic": str(text),
                "score": 1.0
            })

    return out


# -------------------------
# ORCHESTRATOR
# -------------------------

class Orchestrator:

    def __init__(self):
        self.cycle = 0

    def run_cycle(self):

        start = time.time()
        self.cycle += 1

        logger.info(f"[ORCHESTRATOR] Cycle {self.cycle} started")

        try:
            # 1. DATA
            raw = crawl()

            if not raw:
                if LAST_DATA:
                    raw = LAST_DATA
                else:
                    raw = [{"title": "fallback signal"}]

            raw = process_data(raw)

            LAST_DATA.clear()
            LAST_DATA.extend(raw[:100])

            # 2. SIGNALS
            signals = detect_signals(raw)

            if not signals:
                signals = force_signals(raw)

            # 3. RANK
            signals = merge_ranked_signals(signals)

            # 4. INTELLIGENCE
            intel = enrich_intelligence(signals)

            # 5. IMPORTANCE
            intel = compute_importance(intel)

            # 6. DECISION
            intel = run_decision_pipeline(intel)

            # 7. GENERATE
            self._generate(intel)

        except Exception:
            traceback.print_exc()

        finally:
            duration = round(time.time() - start, 2)
            logger.info(f"[ORCHESTRATOR] Cycle finished in {duration}s")

    # -------------------------
    # GENERATION
    # -------------------------

    def _generate(self, items):

        generated = 0

        for intel in items:

            topic = str(intel.get("topic", "")).strip()

            if len(topic) < 5:
                continue

            if is_duplicate(topic):
                continue

            content = safe_generate(intel)

            title = content.get("title")
            body = content.get("content")

            if not title or not body:
                continue

            try:
                save_post(title, body)
            except:
                continue

            generated += 1

            logger.info(f"[ORCHESTRATOR] GENERATED: {topic}")

        if generated == 0:
            logger.warning("[ORCHESTRATOR] NOTHING GENERATED")
