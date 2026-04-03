import time
import traceback

def start():

    try:
        from backend.orchestrator import Orchestrator
        orchestrator = Orchestrator()
    except Exception as e:
        print("ORCHESTRATOR LOAD ERROR:", e)
        traceback.print_exc()
        return

    while True:
        try:
            orchestrator.run_cycle()
            time.sleep(30)
        except Exception:
            traceback.print_exc()
            time.sleep(10)
