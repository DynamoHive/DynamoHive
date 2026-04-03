# backend/auto_content_loop.py

import time
from backend.orchestrator import Orchestrator

orchestrator = Orchestrator()

def start():
    while True:
        orchestrator.run_cycle()
        time.sleep(30)
