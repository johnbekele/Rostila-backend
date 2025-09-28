# Auth business logic
from app.models.auth import RefreshToken
from app.schemas.auth_schema import TokenResponse, UserProfile ,LoginResponse
from app.repositories.user_repository import UserRepository 
from app.core.security import security_manager
from app.services.user_service import UserService
from fastapi import HTTPException, status ,Request
from datetime import timedelta, datetime
from typing import Any, Dict, List, Optional
from app.core.config import settings
from app.utils.helpers import Helpers

class AuthService:
    def __init__(self) -> None:
        self.user_repository = UserRepository()
        self.user_service = UserService()

    async def login__user(
        self, username: str, password: str, client_info: Dict[str, Any]
    ) -> LoginResponse:

  
        authenticated_user = await self.user_service.authenticate_user(
            username, password
        )
       #extract client info
        client_ip = client_info.headers.get("x-forwarded-for") or client_info.client.host
        raw_user_agent = client_info.headers.get("user-agent", "unknown")
        device_info = Helpers.get_device_info(raw_user_agent)

        print(f"client_ip: {client_ip}")
        print(f"device_info: {device_info}")
        print(f"authenticated_user: {authenticated_user}")

        if not authenticated_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # as it's optional we can also leave it open so it will defal to ENV value from settings

        access_token = security_manager.create_access_token(
            data={"sub": authenticated_user.username},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        refresh_token = security_manager.create_refresh_token(
            data={"sub": authenticated_user.username}
        )

        refresh_token_doc = RefreshToken(
            user_id=str(authenticated_user.id),
            token=refresh_token,
            expires_at=datetime.utcnow() + timedelta(days=7),
            is_active=True,
            ip_address=client_ip,
            device_info=device_info.device,
        )

        await refresh_token_doc.insert()

        user_profile = UserProfile(
            id=str(authenticated_user.id),
            email=authenticated_user.email,
            username=authenticated_user.username,
            first_name=authenticated_user.first_name,
            last_name=authenticated_user.last_name,
            is_active=authenticated_user.is_active,
            created_at=authenticated_user.created_at,
            last_login=authenticated_user.last_login,
            last_ip=client_info.get("ip_address") if client_info else None,
            last_device=client_info.get("device_info") if client_info else None,
        )

        return LoginResponse(
            token=access_token, 
            token_type="bearer",
            expires_at=datetime.utcnow() + timedelta(days=7),
            user=user_profile
        )

    async def logout_user(self, refresh_token: str) -> bool:
        try:
            await RefreshToken.find_one(RefreshToken.token == refresh_token).delete()
            return True
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to logout user",
            )

    async def verify_email(self, token: str) -> dict:
        """Verify user email using verification token"""
        # Find user by verification token
        user = await self.user_repository.find_one(verification_token=token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired verification token",
            )

        if user.is_verified:
            return {"message": "User already verified"}

        # Update user verification status
        user.is_verified = True
        user.verification_token = None  # Clear the token after verification
        await user.save()

        return {
            "message": "Email verified successfully",
            "isVerified": user.is_verified,
        }

    async def resend_verification_email(self, email: str) -> dict:
        print(f"email: {email}")
        user = await self.user_repository.email_exists(email)
        print(f"user: {user}")
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
            )
        if user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User already verified"
            )
        return {"message": "Verification email sent successfully"}
    
    async def find_user(self, token: str) -> dict:
        # Decode the token to get the username
        response = security_manager.decode_token(token)
        payload = response.get("payload")
        message = response.get("message")
        success = response.get("success")
        username = payload.get("sub")
        
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Find the user in the database
        user = await self.user_repository.get_user_by_username(username)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Return user data
        return {
            "success": True,
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_verified": user.is_verified,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None
        }
