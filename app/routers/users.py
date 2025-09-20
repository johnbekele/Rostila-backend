from fastapi import APIRouter
from typing import List
from app.schemas import User, UserCreate

router = APIRouter(prefix="/users", tags=["users"])

# Mock database
users_db = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
]

@router.get("/")
def get_users():
    dict_users={}
    for user in users_db:
       dict_users.update({user["id"]:user})
   
    return dict_users

@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        return {"error": "User not found"}
    return user

@router.post("/", response_model=User)
def create_user(user: UserCreate):
    new_user = {"id": len(users_db) + 1, **user.dict()}
    users_db.append(new_user)
    return new_user