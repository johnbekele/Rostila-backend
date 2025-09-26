# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from typing import Optional
import os
from pathlib import Path
from dotenv import load_dotenv

# Get the directory containing this file
BASE_DIR = Path(__file__).resolve().parent.parent

# Load only the app-level .env once (so Pydantic picks it up)
APP_ENV_FILE = BASE_DIR / ".env"
if APP_ENV_FILE.exists():
    print(f"Loading env file: {APP_ENV_FILE}")
    load_dotenv(dotenv_path=APP_ENV_FILE, override=True)


class Settings(BaseSettings):
    # MongoDB Atlas settings
    mongodb_url: str = Field(
        default_factory=lambda: os.getenv("MONGODB_URL", ""), env="MONGODB_URL"
    )
    database_name: str = Field(default="rostila_db", env="DATABASE_NAME")

    # Connection pool settings
    mongodb_max_connections: int = Field(default=10, env="MONGODB_MAX_CONNECTIONS")
    mongodb_min_connections: int = Field(default=1, env="MONGODB_MIN_CONNECTIONS")
    mongodb_max_idle_time_ms: int = Field(default=30000, env="MONGODB_MAX_IDLE_TIME_MS")

    # JWT Settings - Fixed the environment variable names
    SECRET_KEY: str = Field(
        default="e01b8d37762ae6c28f61309774ace021be5521d694eb24c0a3f43ebdb76a2f39",
        env="SECRET_KEY",
    )
    REFRESH_SECRET_KEY: str = Field(
        default="dev_refresh_key_please_change_me_32_charsminxxxx",
        env="REFRESH_SECRET_KEY",
    )
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
    FRONTEND_URL: str = Field(default="http://localhost:3000", env="FRONTEND_URL")
    BACKEND_URL: str = Field(default="http://localhost:8000", env="BACKEND_URL")

    @field_validator("debug", mode="before")
    def parse_debug(cls, v):
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes", "on")
        return bool(v)

    @field_validator("mongodb_url")
    def validate_mongodb_url(cls, v):
        if not v or v == "None":
            raise ValueError("MONGODB_URL is required")
        return v

    @field_validator("SECRET_KEY", "REFRESH_SECRET_KEY")
    def validate_secrets(cls, v):
        if not v or v == "None" or len(v) < 32:
            raise ValueError("Secret keys must be at least 32 characters long")
        return v

    # Pydantic v2 settings configuration
    model_config = SettingsConfigDict(
        env_file=str(APP_ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Ignore unrelated env vars (e.g., DOPPLER_*)
    )


settings = Settings()
