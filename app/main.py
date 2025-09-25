from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_database, close_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to MongoDB
    await init_database()
    yield
    # Shutdown: Close MongoDB connection
    await close_database()


app = FastAPI(lifespan=lifespan)

# routes
from app.routers import users
from app.routers import auth

app.include_router(users.router, tags=["users"], prefix="/api/users")
app.include_router(auth.router, tags=["auth"], prefix="/api/auth")
