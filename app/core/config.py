from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path
from dotenv import load_dotenv  # Fixed import

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
        load_dotenv(dotenv_path=env_file, override=False)

class Settings(BaseSettings):
    # MongoDB Atlas settings
    mongodb_url: str =str( os.getenv("MONGODB_URL"))  
    database_name: str = str(os.getenv("DATABASE_NAME") )
    
    # Connection pool settings
    mongodb_max_connections: int = int(os.getenv("MONGODB_MAX_CONNECTIONS", "10"))
    mongodb_min_connections: int = int(os.getenv("MONGODB_MIN_CONNECTIONS", "1"))
    mongodb_max_idle_time_ms: int = int(os.getenv("MONGODB_MAX_IDLE_TIME_MS", "30000"))
  
    # JWT Settings
    SECRET_KEY: str = str(os.getenv("CLIENT_SECRET"))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Email (for password reset)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None

    # App settings
    app_name: str = os.getenv("APP_NAME", "Rostila Backend")
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()