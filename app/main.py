from fastapi import FastAPI
from app.routers import users

app = FastAPI(title="My FastAPI App", version="1.0.0")

# Include routers
app.include_router(users.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}