 # Environment config (like .env handling)import motor.motor_asyncio
from app.config import settings

# Create MongoDB client (similar to mongoose.connect())
client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongodb_url)
database = client[settings.database_name]

# Collections (like your MongoDB collections)
user_collection = database.get_collection("users")
post_collection = database.get_collection("posts")

# Helper function to get database
async def get_database():
    return database