# models/user.py
from beanie import Document, Indexed
from pydantic import EmailStr, Field
from datetime import datetime
from typing import Optional
from pymongo import IndexModel


class User(Document):
    """
    User model - like Mongoose schema
    Beanie handles _id automatically
    """

    email: Indexed(EmailStr, unique=True)
    username: Indexed(str, unique=True)
    hashed_password: str
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    company_name: Optional[str] = None
    company_address: Optional[str] = None
    company_phone_number: Optional[str] = None
    company_email: Optional[str] = None
    company_website: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    verification_token: Optional[str] = None
    last_login: Optional[datetime] = None
    last_ip: Optional[str] = None
    last_device: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Settings:
        # Collection name (like Mongoose model name)
        collection = "users"

        # Indexes (like Mongoose indexes)
        indexes = [
            IndexModel("email", unique=True),
            IndexModel("username", unique=True),
            "created_at",
        ]

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
