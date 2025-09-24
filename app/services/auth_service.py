  # Auth business logic
from app.models.auth import RefreshToken 
from app.schemas.authSChema import TokenResponse
from app.repositories.user_repository import UserRepository
from core.security import security_manager
from app.services.user_service import UserService
from fastapi import HTTPException ,status
from datetime import timedelta ,datetime
from typing import Any ,Dict ,List 
from app.core.config import settings

class AuthService:
  def __init__(self) -> None:
     self.user_repository=UserRepository()
     self.user_service=UserService()

  async def login__user(self,username:str,password:str , client_info: Dict[str, Any] )-> TokenResponse:
      
      authenticated_user=await self.user_service.authenticate_user(username,password)

      if not authenticated_user:
         raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
         )
      
      # as it's optional we can also leave it open so it will defal to ENV value from settings
      
      access_token=security_manager.create_access_token(
         data=authenticated_user,
         expires_delta=timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)) 
      
      refresh_token=security_manager.create_refresh_token(
         data=authenticated_user
      )
       
      refresh_token_doc = RefreshToken(
         user_id=authenticated_user.id,
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