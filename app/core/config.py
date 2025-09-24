# app/core/config.py
from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import Optional
import os
from pathlib import Path
from dotenv import load_dotenv

# Get the directory containing this file
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment-specific .env file
environment = os.getenv("ENVIRONMENT", "development")
env_files = [
    BASE_DIR / f".env.{environment}",  # .env.development, .env.production
    BASE_DIR / ".env.local",           # Local overrides
    BASE_DIR / ".env"                  # Default
]

# Load env files in order (later files override earlier ones)
for env_file in env_files:
    if env_file.exists():
        print(f"Loading env file: {env_file}")  # Debug info
        load_dotenv(dotenv_path=env_file, override=False)

class Settings(BaseSettings):
    # MongoDB Atlas settings
    mongodb_url: str = Field(..., env="MONGODB_URL")  # Required field
    database_name: str = Field(..., env="DATABASE_NAME")  # Required field
    
    # Connection pool settings
    mongodb_max_connections: int = Field(default=10, env="MONGODB_MAX_CONNECTIONS")
    mongodb_min_connections: int = Field(default=1, env="MONGODB_MIN_CONNECTIONS") 
    mongodb_max_idle_time_ms: int = Field(default=30000, env="MONGODB_MAX_IDLE_TIME_MS")
  
    # JWT Settings - Fixed the environment variable names
    SECRET_KEY: str = Field(..., env="SECRET_KEY")  # Changed from CLIENT_SECRET
    REFRESH_SECRET_KEY: str = Field(..., env="REFRESH_SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Email (for password reset)
    SMTP_HOST: Optional[str] = Field(default=None, env="SMTP_HOST")
    SMTP_PORT: Optional[int] = Field(default=None, env="SMTP_PORT")
    SMTP_USER: Optional[str] = Field(default=None, env="SMTP_USER")
    SMTP_PASSWORD: Optional[str] = Field(default=None, env="SMTP_PASSWORD")

    # App settings
    app_name: str = Field(default="Rostila Backend", env="APP_NAME")
    debug: bool = Field(default=True, env="DEBUG")
    environment: str = Field(default="development", env="ENVIRONMENT")
    
    @validator('debug', pre=True)
    def parse_debug(cls, v):
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes", "on")
        return bool(v)
    
    @validator('mongodb_url')
    def validate_mongodb_url(cls, v):
        if not v or v == "None":
            raise ValueError("MONGODB_URL is required")
        return v
    
    @validator('SECRET_KEY', 'REFRESH_SECRET_KEY')
    def validate_secrets(cls, v):
        if not v or v == "None" or len(v) < 32:
            raise ValueError("Secret keys must be at least 32 characters long")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True  # Keep case sensitivity for consistency

settings = Settings()