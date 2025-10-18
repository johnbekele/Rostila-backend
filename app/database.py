# app/database.py
import motor.motor_asyncio
from beanie import init_beanie
import os

# from dotenv import load_dotenv
from app.models.users import User
from app.models.auth import RefreshToken, PasswordResetToken
from app.models.coffee import Coffee
from app.core.config import settings
import certifi

# Load environment variables from .env file
# load_dotenv()


MONGODB_URL = settings.mongodb_url
DATABASE_NAME = settings.database_name

print(
    f"My mongo URL: [redacted] (scheme: {'mongodb+srv' if MONGODB_URL.startswith('mongodb+srv') else 'mongodb'})"
)
print(f"Database name: {DATABASE_NAME}")

if not MONGODB_URL:
    print("⚠️  MONGODB_URL is not set; skipping database initialization.")

client = None


async def init_database():
    """Initialize MongoDB connection with ALL collections"""
    global client

    try:
        # Create motor client
        client = motor.motor_asyncio.AsyncIOMotorClient(
            MONGODB_URL, tlsCAFile=certifi.where()
        )

        # Test connection
        await client.admin.command("ping")

        # Use specific database name instead of get_default_database()
        database = client[DATABASE_NAME]

        # Initialize beanie with ALL document models
        await init_beanie(
            database=database, document_models=[User, RefreshToken, PasswordResetToken, Coffee]
        )

        print("🍃 Connected to MongoDB Atlas!")

    except Exception as e:
        print(f"❌ Failed to connect to MongoDB Atlas: {e}")
        # Do not crash the app if DB is unavailable in dev
        if os.getenv("ALLOW_START_WITHOUT_DB", "true").lower() in (
            "1",
            "true",
            "yes",
            "on",
        ):
            print(
                "🚧 Continuing without database connection (ALLOW_START_WITHOUT_DB=true)"
            )
            return
        else:
            raise


async def close_database():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        print("🍃 Disconnected from MongoDB Atlas")
