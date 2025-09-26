# schemas/user.py
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @validator("email")
    def email_must_be_valid(cls, v):
        if "@" not in v:
            raise ValueError("Email must contain @ symbol")
        if len(v) < 5:
            raise ValueError("Email must be at least 5 characters")
        return v

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class LoginResponse(BaseModel):
    token: str
    token_type: str = "bearer"
    expires_at: datetime


class TokenPayload(BaseModel):
    sub: str  # user_id
    exp: datetime
    iat: datetime
    type: str  # "access" or "refresh"


class PasswordResetRequest(BaseModel):
    """Password reset request schema"""

    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation schema"""

    token: str
    new_password: str


class ChangePasswordRequest(BaseModel):
    """Change password request schema"""

    current_password: str
    new_password: str


class UserProfile(BaseModel):
    """User profile response schema"""

    id: str
    email: str
    username: str
    first_name: str
    last_name: str
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None


# TokenResponse
class TokenResponse(BaseModel):
    """Response model for authentication tokens"""
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 1800  # 30 minutes in seconds


class RefreshTokenRequest(BaseModel):
    """Request model for token refresh"""

    refresh_token: str

    @validator("refresh_token")
    def validate_refresh_token(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Refresh token cannot be empty")
        return v.strip()


class ResendVerificationEmailRequest(BaseModel):
    email: str
