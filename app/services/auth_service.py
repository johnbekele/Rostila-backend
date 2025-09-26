# Auth business logic
from app.models.auth import RefreshToken
from app.schemas.authSChema import TokenResponse, UserProfile
from app.repositories.user_repository import UserRepository 
from app.core.security import security_manager
from app.services.user_service import UserService
from fastapi import HTTPException, status
from datetime import timedelta, datetime
from typing import Any, Dict, List, Optional
from app.core.config import settings


class AuthService:
    def __init__(self) -> None:
        self.user_repository = UserRepository()
        self.user_service = UserService()

    async def login__user(
        self, username: str, password: str, client_info: Dict[str, Any]
    ) -> TokenResponse:

        authenticated_user = await self.user_service.authenticate_user(
            username, password
        )

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
            ip_address=client_info.get("ip_address") if client_info else None,
            device_info=client_info.get("device_info") if client_info else None,
            user_agent=client_info.get("user_agent") if client_info else None,
        )

        await refresh_token_doc.insert()

        return TokenResponse(
            access_token=access_token, 
            refresh_token=refresh_token, 
            token_type="bearer"
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
    
    async def find_user(self,token:str)-> str:
        user= security_manager.decode_token(token)
       
        return str(user)
