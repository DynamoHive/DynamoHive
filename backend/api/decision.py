from fastapi import APIRouter

router = APIRouter()


@router.get("/decision")
def decision():

    return {
        "decision_engine": "active",
        "autonomous_mode": True
    }
