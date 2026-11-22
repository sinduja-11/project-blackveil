
from fastapi import FastAPI

from config.settings import settings


# Create the FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Adaptive Deception and Intelligence Defence for Permissioned Blockchains",
    version="0.1.0"
)


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
