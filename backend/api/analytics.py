from fastapi import APIRouter

from backend.storage import count_signals

router = APIRouter()


@router.get("/analytics")
def analytics():

    total = count_signals()

    return {
        "total_signals": total,
        "status": "active"
    }
