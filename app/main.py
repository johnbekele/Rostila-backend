from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routes
from app.routers import users
from app.routers import auth
from app.routers import genai
from app.routers import product

app.include_router(users.router, tags=["users"], prefix="/api/users")
app.include_router(auth.router, tags=["auth"], prefix="/api/auth")
app.include_router(genai.router, tags=["genai"], prefix="/api/genai")
app.include_router(product.router, tags=["product"], prefix="/api/product")