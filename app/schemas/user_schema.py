# schemas/user.py
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    first_name: str
    last_name: str
    phone_number: str
    company_name: str
    company_address: str
    company_phone_number: str
    company_email: str
    company_website: str

    @field_validator("username")
    @classmethod
    def username_must_be_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError("Username must be alphanumeric")
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class UserResponse(BaseModel):
    id: str  # MongoDB ObjectId as string
    email: str
    username: str
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    company_name: Optional[str] = None
    company_address: Optional[str] = None
    company_phone_number: Optional[str] = None
    company_email: Optional[str] = None
    company_website: Optional[str] = None
    is_active: bool
    is_verified: bool
    last_login: Optional[datetime] = None
    last_ip: Optional[str] = None
    last_device: Optional[str] = None
    created_at: datetime

    class Config:
        # For Beanie models
        arbitrary_types_allowed = True


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
