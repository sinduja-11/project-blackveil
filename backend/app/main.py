
from fastapi import FastAPI

from config.settings import settings
from app.identity.router import router as identity_router


# Create the FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Adaptive Deception and Intelligence Defence for Permissioned Blockchains",
    version="0.1.0"
)

# Mount routers
app.include_router(identity_router)


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Welcome to PROJECT BLACKVEIL",
        "status": "running"
    }


# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "project": settings.app_name,
        "status": "healthy",
        "environment": settings.app_env
    }
