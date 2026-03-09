from fastapi import APIRouter
from backend.data_pipeline import add_event

router = APIRouter()

users = []

@router.post("/users")
def create_user(username: str):

    user = {
        "id": len(users) + 1,
        "username": username
    }

    users.append(user)

    add_event({
        "type": "user_signup",
        "user_id": user["id"]
    })

    return user


@router.get("/users")
def list_users():
    return users
