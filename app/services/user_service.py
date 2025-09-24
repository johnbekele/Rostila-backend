from app.repositories.user_repository import UserRepository
from app.schemas.users import UserCreate, UserResponse 
from fastapi import HTTPException, status
from typing import Optional, List, Dict, Any 
from core.security import security_manager
from  app.models.users import User

class UserService:
    def __init__(self) -> None:
        self.user_repository = UserRepository()
  
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """Create user using base repository methods"""
        
        # Check if email already exists
        if await self.user_repository.email_exists(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Email already exists"
            )
        
        # Check if username already exists
        if await self.user_repository.username_exists(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Username already exists"
            )
        
        # Use security_manager for consistent password hashing
        hashed_password = security_manager.get_password_hash(user_data.password)
        
        # Create user
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
    
    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user by username or email"""
        
        # Try to find user by username first
        user = await self.user_repository.username_exists(username)
        
        # If not found by username, try by email
        if not user:
            user = await self.user_repository.email_exists(username)
        
        # If user still not found
        if not user:
            return None
        
       
            # Fallback for direct dict access
     
        
        # Verify password
        if not security_manager.verify_password(password, user["hashed_password"]):
            return None
        
        # Check if user is active
        if not user.get("is_active", True):
            return None
            
        return user

    async def get_user_by_id(self, user_id: str) -> UserResponse:  # Fixed indentation
        """Get user by ID"""
        user = await self.user_repository.find_by_ID(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse(
            id=str(user.id),
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            created_at=user.created_at
        )
    
    async def get_user_by_email(self, email: str) -> UserResponse:
        """Get user by email"""
        user = await self.user_repository.email_exists(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse(
            id=str(user.id),
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            created_at=user.created_at
        )

    async def get_user_by_username(self, username: str) -> UserResponse:
        """Get user by username"""
        user = await self.user_repository.username_exists(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse(
            id=str(user.id),
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            created_at=user.created_at
        )

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """Get all users with pagination"""
        users = await self.user_repository.get_all_users(skip=skip, limit=limit)
        return [
            UserResponse(
                id=str(user.id),
                email=user.email,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                is_active=user.is_active,
                created_at=user.created_at
            )
            for user in users
        ]

    async def update_user(self, user_id: str, update_data: Dict[str, Any]) -> UserResponse:
        """Update user information"""
        user = await self.user_repository.find_by_ID(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Remove password from update_data 
        if 'password' in update_data:
            update_data.pop('password')
        
        # Update user
        try:
            updated_user = await self.user_repository.update_user_by_id(user_id, update_data)
        
        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user"
            )
        
        return UserResponse(
            id=str(updated_user.id),
            email=updated_user.email,
            username=updated_user.username,
            first_name=updated_user.first_name,
            last_name=updated_user.last_name,
            is_active=updated_user.is_active,
            created_at=updated_user.created_at
        )

    async def deactivate_user(self, user_id: str) -> UserResponse:
        """Deactivate user instead of deleting"""
        user = await self.user_repository.find_by_ID(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        updated_user = await self.user_repository.update_user_by_id(
            user_id, 
            {"is_active": False}
        )
        
        return UserResponse(
            id=str(updated_user.id),
            email=updated_user.email,
            username=updated_user.username,
            first_name=updated_user.first_name,
            last_name=updated_user.last_name,
            is_active=updated_user.is_active,
            created_at=updated_user.created_at
        )

    async def change_password(self, user_id: str, new_password: str) -> bool:
        """Change user password"""
        user = await self.user_repository.find_by_ID(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        hashed_password = security_manager.get_password_hash(new_password)
        await self.user_repository.update_user_by_id(
            user_id, 
            {"hashed_password": hashed_password}
        )
        
        return True