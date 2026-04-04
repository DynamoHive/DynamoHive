import time
import traceback

from backend.logger import logger

# SAFE IMPORT
def safe_import(module_path, attr=None):
    try:
        module = __import__(module_path, fromlist=[attr] if attr else [])
        return getattr(module, attr) if attr else module
    except Exception as e:
        print(f"[IMPORT ERROR] {module_path}.{attr} -> {e}")
        return None


# -------------------------
# IMPORTS
# -------------------------
crawl = safe_import("ai_engine.multi_crawler", "crawl")
process_data = safe_import("ai_engine.data_pipeline", "process_data")
signal_module = safe_import("ai_engine.signal_detector")

generate_narrative = safe_import("ai_engine.narrative_engine", "generate_narrative")

save_post = safe_import("backend.storage", "save_post")
distribute = safe_import("backend.distribution_engine", "distribute")


# -------------------------
# ORCHESTRATOR
# -------------------------
class Orchestrator:

    def __init__(self):
        self.cycle_count = 0

    def run_cycle(self):

        self.cycle_count += 1
        logger.info(f"[ORCHESTRATOR] Cycle {self.cycle_count} started")

        try:
            # -------------------------
            # DATA
            # -------------------------
            raw_data = []

            if crawl:
                try:
                    raw_data = crawl()
                except Exception as e:
                    logger.warning(f"[CRAWL ERROR] {e}")

            if process_data:
                try:
                    raw_data = process_data(raw_data)
                except Exception as e:
                    logger.warning(f"[PIPELINE ERROR] {e}")

            # -------------------------
            # SIGNAL
            # -------------------------
            signals = []

            if signal_module and hasattr(signal_module, "detect_signals"):
                try:
                    signals = signal_module.detect_signals(raw_data)
                except Exception as e:
                    logger.warning(f"[SIGNAL ERROR] {e}")

            logger.info(f"[SIGNALS] {len(signals)}")

            # -------------------------
            # CONTENT
            # -------------------------
            self._generate_content(signals)

        except Exception:
            traceback.print_exc()

        finally:
            logger.info("[ORCHESTRATOR] Cycle finished")


    # -------------------------
    # CONTENT
    # -------------------------
    def _generate_content(self, signals):

        if not signals:
            logger.info("[CONTENT] no signals")
            return

        for s in signals:

            topic = str(s.get("topic", "")).strip()

            if not topic:
                continue

            try:
                if generate_narrative:
                    content = generate_narrative(s)
                else:
                    content = {"title": topic, "content": topic}
            except Exception as e:
                logger.warning(f"[NARRATIVE ERROR] {e}")
                continue

            if not content:
                continue

            title = content.get("title")
            body = content.get("content")

            if not title or not body:
                continue

            try:
                if save_post:
                    save_post(title, body)
            except Exception as e:
                logger.warning(f"[SAVE ERROR] {e}")

            try:
                if distribute:
                    distribute(content)
            except Exception as e:
                logger.warning(f"[DISTRIBUTION ERROR] {e}")

            logger.info(f"[GENERATED] {topic}")
