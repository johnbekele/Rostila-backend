# schemas/user.py
from pydantic import BaseModel, EmailStr, validator
from typing import Optional ,List
from datetime import datetime

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
    
    @validator('email')
    def email_must_be_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

class LoginResponse (BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
    user: dict  # User info
    
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