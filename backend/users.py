from fastapi import APIRouter

router = APIRouter()

users = []

@router.post("/users/register")
def register_user(username: str):
    user = {"id": len(users) + 1, "username": username}
    users.append(user)
    return user

@router.get("/users")
def list_users():
    return users
