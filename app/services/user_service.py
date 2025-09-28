from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserResponse
from fastapi import HTTPException, status
from typing import Optional, List, Dict, Any
from app.core.security import security_manager
from app.models.users import User
from app.services.email_service import EmailService
from app.core.config import settings


class UserService:
    def __init__(self) -> None:
        self.user_repository = UserRepository()

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        existing_user = await self.user_repository.email_exists(user_data.email)
        username_exists = await self.user_repository.username_exists(user_data.username)

        # Case 1: Email exists
        if existing_user:
            if existing_user.is_verified:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Account already exists",
                )
            else:
                # Resend verification link
                try:
                    email_service = EmailService()
                    verification_link = f"{settings.BACKEND_URL}/api/auth/verify-email?token={existing_user.verification_token}"
                    body = email_service.get_template("email_verification")
                    body = body.replace("[Verification Link]", verification_link)
                    body = body.replace("[User Name]", existing_user.username)

                    await email_service.send_email(
                        to_email=existing_user.email,
                        subject="Email Verification - Resent",
                        body=body,
                    )
                    return UserResponse(
                        id=str(existing_user.id),
                        email=existing_user.email,
                        username=existing_user.username,
                        first_name=existing_user.first_name,
                        last_name=existing_user.last_name,
                        is_active=existing_user.is_active,
                        created_at=existing_user.created_at,
                    )
                except Exception as e:
                    print(f"Failed to resend verification email: {e}")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Could not resend verification email",
                    )

        # Case 2: Username exists
        if username_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
            )

        # Case 3: Fresh signup
        hashed_password = security_manager.get_password_hash(user_data.password)
        user = await self.user_repository.create_user(user_data, hashed_password)

        try:
            email_service = EmailService()
            verification_link = f"{settings.BACKEND_URL}/api/auth/verify-email?token={user.verification_token}"
            body = email_service.get_template("email_verification")
            body = body.replace("[Verification Link]", verification_link)
            body = body.replace("[User Name]", user.username)

            await email_service.send_email(
                to_email=user.email, subject="Email Verification", body=body
            )
            print(f"Verification email sent to {user.email}")
        except Exception as e:
            print(f"Failed to send verification email: {e}")

        return UserResponse(
            id=str(user.id),
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            created_at=user.created_at,
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

        # Verify password
        if not security_manager.verify_password(password, user.hashed_password):
            return None

        # Check if user is active
        if not user.is_active:
            return None

        return user

    async def get_user_by_id(self, user_id: str) -> UserResponse:
        """Get user by ID"""
        user = await self.user_repository.find_by_ID(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return UserResponse(
            id=str(user.id),
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            created_at=user.created_at,
        )

    async def get_user_by_email(self, email: str) -> UserResponse:
        """Get user by email"""
        user = await self.user_repository.email_exists(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return UserResponse(
            id=str(user.id),
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            created_at=user.created_at,
        )

    async def get_user_by_username(self, username: str) -> UserResponse:
        """Get user by username"""
        user = await self.user_repository.username_exists(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return UserResponse(
            id=str(user.id),
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            created_at=user.created_at,
        )

    async def get_all_users(
        self, skip: int = 0, limit: int = 100
    ) -> List[UserResponse]:
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
                created_at=user.created_at,
            )
            for user in users
        ]

    async def update_user(
        self, user_id: str, update_data: Dict[str, Any]
    ) -> UserResponse:
        """Update user information"""
        user = await self.user_repository.find_by_ID(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        # Remove password from update_data
        if "password" in update_data:
            update_data.pop("password")

        # Update user
        try:
            updated_user = await self.user_repository.update_user_by_id(
                user_id, update_data
            )

        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user",
            )

        return UserResponse(
            id=str(updated_user.id),
            email=updated_user.email,
            username=updated_user.username,
            first_name=updated_user.first_name,
            last_name=updated_user.last_name,
            is_active=updated_user.is_active,
            created_at=updated_user.created_at,
        )

    async def deactivate_user(self, user_id: str) -> UserResponse:
        """Deactivate user instead of deleting"""
        user = await self.user_repository.find_by_ID(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        updated_user = await self.user_repository.update_user_by_id(
            user_id, {"is_active": False}
        )

        return UserResponse(
            id=str(updated_user.id),
            email=updated_user.email,
            username=updated_user.username,
            first_name=updated_user.first_name,
            last_name=updated_user.last_name,
            is_active=updated_user.is_active,
            created_at=updated_user.created_at,
        )

    async def change_password(self, user_id: str, new_password: str) -> bool:
        """Change user password"""
        user = await self.user_repository.find_by_ID(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        hashed_password = security_manager.get_password_hash(new_password)
        await self.user_repository.update_user_by_id(
            user_id, {"hashed_password": hashed_password}
        )

        return True
