# app/database.py
import motor.motor_asyncio
from beanie import init_beanie
import os
from dotenv import load_dotenv
from app.models.users import User
from app.core.config import settings

# Load environment variables from .env file
load_dotenv()


    


MONGODB_URL = settings.mongodb_url
DATABASE_NAME = settings.database_name

print(f"My mongo URL: {MONGODB_URL}")
print(f"Database name: {DATABASE_NAME}")

if not MONGODB_URL:
    raise ValueError("MONGO_URI environment variable is not set")

client = None

async def init_database():
    """Initialize MongoDB connection with ALL collections"""
    global client
    
    try:
        # Create motor client
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
        
        # Test connection
        await client.admin.command('ping')
        
        # Use specific database name instead of get_default_database()
        database = client[DATABASE_NAME]
        
        # Initialize beanie with ALL document models
        await init_beanie(
            database=database,
            document_models=[
                User,
            ]
        )
        
        print("🍃 Connected to MongoDB Atlas!")
        
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB Atlas: {e}")
        raise

async def close_database():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        print("🍃 Disconnected from MongoDB Atlas")