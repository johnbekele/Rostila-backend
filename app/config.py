import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    mongodb_url: str = os.get
    database_name: str = "Rostila"
    secret_key: str = "your-secret-key-here"
    
    class Config:
        env_file = ".env"

settings = Settings()