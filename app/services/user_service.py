from app.repositories.user_repository import UserRepository
from  app.schemas.users import UserCreate ,UserResponse 
from fastapi import HTTPException ,status
from passlib.context import CryptContext
from typing import Optional ,List

#hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService():
    def __init__(self) -> None:
       self.user_repository=UserRepository()
  
    async def create_user(self, user_data: UserCreate) -> UserResponse:
       """Create user using base repository methods"""
       
       # Use base repository methods
       if await self.user_repository.email_exists(user_data.email):
           raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email already exists")
       
       if await self.user_repository.username_exists(user_data.username):
           raise HTTPException(status.HTTP_400_BAD_REQUEST, "Username already exists")
       
       hashed_password = pwd_context.hash(user_data.password)
       
       # Use specific repository method
       user = await self.user_repository.create_user(user_data, hashed_password)
       
       return UserResponse(
           id=str(user.id),
           email=user.email,
           username=user.username,
           first_name=user.first_name,
           last_name=user.last_name,
           is_active=user.is_active,
           created_at=user.created_at
       )
    
    #GET UserByID
    async def get_user_by_id(self,user_id:str )->UserResponse:
        user=await self.user_repository.find_by_ID(user_id)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND,"user not found ")
        
        return UserResponse(
            id=str(user.id),
           email=user.email,
           username=user.username,
           first_name=user.first_name,
           last_name=user.last_name,
           is_active=user.is_active,
           created_at=user.created_at
        )
    
    #getuser by email 
    async def get_user_by_email(self,email:str )->UserResponse:
        user=await self.user_repository.email_exists(email)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND,"user not found ")
        
        return UserResponse(
            id=str(user.id),
           email=user.email,
           username=user.username,
           first_name=user.first_name,
           last_name=user.last_name,
           is_active=user.is_active,
           created_at=user.created_at
        )
    


    
    async def get_all_users(self)-> List[UserResponse]:
        users=await self.user_repository.find_all()
        return [UserResponse(
                id=str(user.id),
                email=user.email,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                is_active=user.is_active,
                created_at=user.created_at
        )
        for user in users]