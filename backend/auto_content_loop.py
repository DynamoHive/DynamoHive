import time
import traceback

def start():

    print("🚀 FORCE START")
    print("🔥 ORCHESTRATOR READY")

    while True:

        print("🔁 LOOP TICK")

        try:
            from backend.orchestrator import Orchestrator

            orch = Orchestrator()
            orch.run_cycle()

        except Exception as e:
            print("[LOOP ERROR]", e)
            traceback.print_exc()

        # 🔥 KRİTİK: loop ölmesin
        time.sleep(15)
