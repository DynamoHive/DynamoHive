from fastapi import APIRouter, Header, HTTPException
import time

router = APIRouter()

API_KEY = "CHANGE_ME"

def auth(x_api_key: str | None):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="unauthorized")


@router.get("/intel/latest")
def latest(x_api_key: str = Header(None)):

    auth(x_api_key)

    # burada senin orchestrator output’un olmalı
    from backend.orchestrator import Orchestrator

    orch = Orchestrator()
    data = orch.run_cycle()

    return {
        "status": "ok",
        "count": len(data),
        "data": data,
        "generated_at": int(time.time())
    }


@router.get("/health")
def health():
    return {"status": "ok"}
