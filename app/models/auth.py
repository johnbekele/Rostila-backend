# models/auth.py
from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional

class RefreshToken(Document):
    """Refresh token model for database storage"""
    user_id: str  # Reference to User
    token: str
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True
    device_info: Optional[str] = None  # Browser, device info
    ip_address: Optional[str] = None
    
    class Settings:
        collection = "refresh_tokens"

class PasswordResetToken(Document):
    """Password reset token model"""
    user_id: str
    token: str
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_used: bool = False
    
    class Settings:
        collection = "password_reset_tokens"