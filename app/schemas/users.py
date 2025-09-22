# schemas/user.py
from pydantic import BaseModel, EmailStr, validator
from typing import Optional ,List
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    first_name: str
    last_name: str
    
    @validator('username')
    def username_must_be_alphanumeric(cls, v):
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

class UserResponse(BaseModel):
    id: str  # MongoDB ObjectId as string
    email: str
    username: str
    first_name: str
    last_name: str
    is_active: bool
    created_at: datetime
    
    class Config:
        # For Beanie models
        arbitrary_types_allowed = True

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None


