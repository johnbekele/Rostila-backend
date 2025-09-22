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
    email: Indexed(EmailStr, unique=True)  # Unique index like Mongoose
    username: Indexed(str, unique=True)    # Unique index
    hashed_password: str
    first_name: str
    last_name: str
    is_active: bool = True
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
    
   