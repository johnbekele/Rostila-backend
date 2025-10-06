from ..models.users import User
from ..schemas.user_schema import UserCreate
from ..repositories.base_repository import BaseRepository
from typing import Optional, List, Dict
from beanie import PydanticObjectId
from pymongo.errors import DuplicateKeyError
import secrets


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    async def create_user(self, user_data: UserCreate, hashed_password: str, client_ip: str = None) -> User:
        user_dict = {
            "email": user_data.email,
            "username": user_data.username,
            "hashed_password": hashed_password,
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "phone_number": user_data.phone_number,
            "company_name": user_data.company_name,
            "company_address": user_data.company_address,
            "company_phone_number": user_data.company_phone_number,
            "company_email": user_data.company_email,
            "company_website": user_data.company_website,
            "verification_token": secrets.token_urlsafe(32),
        }
        user = User(**user_dict)
        await user.insert()
        return user

    async def email_exists(self, email: str) -> Optional[User]:

        return await self.find_one(email=email)

    async def username_exists(self, username: str) -> Optional[User]:

        return await self.find_one(username=username)

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return await self.find_all(skip, limit)

    async def update_user_by_id(self, user_id: str, user_data) -> User:
        result = await self.update_one(user_id, user_data)
        if not result:
            raise RuntimeError(
                f"user with id {user_id} doesn't exist or operation failed"
            )
        return result

    async def get_user_by_username(self, username: str) -> Optional[User]:
        return await self.find_one(username=username)

       

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        return await self.find_by_ID(user_id)
