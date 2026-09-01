from ai_engine.v2.state_store import StateStore
from ai_engine.v2.event_bus import EventBus
from ai_engine.v2.signal_queue import SignalQueue
from ai_engine.v2.worker_pool import WorkerPool
from ai_engine.v2.runtime import Runtime
from ai_engine.v2.execution_graph import ExecutionGraph
from ai_engine.v2.orchestrator_v2 import OrchestratorV2

from backend.storage import save_post


# -------------------------
# CORE INIT
# -------------------------
state = StateStore()
bus = EventBus()
queue = SignalQueue()
workers = WorkerPool(worker_count=4)

# -------------------------
# START WORKERS
# -------------------------
workers.start()

# -------------------------
# EXECUTION GRAPH (CRITICAL BINDING)
# -------------------------
graph = ExecutionGraph(
    state=state,
    bus=bus,
    queue=queue,
    worker_pool=workers,
    intelligence_engine=None,   # inject edilecekse buraya bağlanır
    decision_engine=None,       # inject edilecekse buraya bağlanır
    storage=save_post
)

# -------------------------
# RUNTIME
# -------------------------
runtime = Runtime(
    state_store=state,
    event_bus=bus,
    signal_queue=queue,
    worker_pool=workers
)

# -------------------------
# ORCHESTRATOR
# -------------------------
orchestrator = OrchestratorV2(
    state=state,
    bus=bus,
    queue=queue,
    execution_graph=graph
)

# -------------------------
# START SYSTEM
# -------------------------
print("[DYNAMOHIVE V2] STARTING...")

runtime.start()

# -------------------------
# MAIN LOOP
# -------------------------
try:
    while True:
        orchestrator.run_cycle()

except KeyboardInterrupt:
    print("[DYNAMOHIVE V2] STOPPED BY USER")
    runtime.stop()
    workers.stop()
