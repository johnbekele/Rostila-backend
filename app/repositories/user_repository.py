from ..models.users import User
from ..schemas.users import UserCreate
from ..repositories.base import BaseRepository
from typing import Optional, List
from beanie import PydanticObjectId
from pymongo.errors import DuplicateKeyError

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)
      
    async def create_user(self, user_data: UserCreate, hashed_password: str) -> User:
        user_dict = {
            "email": user_data.email,
            "username": user_data.username,
            "hashed_password": hashed_password,
            "first_name": user_data.first_name,
            "last_name": user_data.last_name
        }
        user = User(**user_dict)
        await user.create()
        return user
    
    async def email_exists(self, email: str) -> Optional[User]:
  
        return await self.find_one(email=email)
    
    async def username_exists(self, username: str) -> Optional[User]:
      
        return await self.find_one(username=username)
    
    async def get_all_users(self,skip:int =0 , limit:int=100)->List[User]:
        return await self.find_all(skip,limit)
    

