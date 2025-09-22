from fastapi import APIRouter, Depends
from app.services.user_service import UserService
from app.schemas.users import UserCreate

router = APIRouter()

def get_user_service() -> UserService:
    return UserService()

@router.get("/")
async def get_users(user_service: UserService = Depends(get_user_service)):
    return await user_service.get_all_users()

@router.post("/")
async def create_user(user_data: UserCreate,user_service:UserService=Depends(get_user_service)):
    return await user_service.create_user(user_data)

@router.post("/{email}")
async def getUser_byemail(email:str,user_service:UserService=Depends(get_user_service)):
    print("find Function invoked")
    return await user_service.get_user_by_email(email)