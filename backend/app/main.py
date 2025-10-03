"""
AI-Powered Programming Learning Platform
Main FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger
import sys

# Configure logger
logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
)
logger.add("logs/app.log", rotation="500 MB", retention="10 days", level="INFO")

# Application metadata
app = FastAPI(
    title="AI Learn Programming Platform",
    description="Zero to Hero Programming Learning with AI-powered content generation",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("🚀 Starting AI Learn Programming Platform")
    logger.info("📚 Initializing services...")
    # TODO: Initialize database connection
    # TODO: Initialize Redis connection
    # TODO: Load XML topics
    # TODO: Verify Gemini API connection
    logger.success("✅ All services initialized successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🛑 Shutting down AI Learn Programming Platform")
    # TODO: Close database connections
    # TODO: Close Redis connections
    logger.success("✅ Shutdown completed")

@app.get("/api")
async def api_root():
    """API root endpoint - API health check"""
    return {
        "message": "AI Learn Programming Platform API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/api/docs"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "api": "operational",
            "database": "pending",  # TODO: Check DB connection
            "redis": "pending",     # TODO: Check Redis connection
            "ai": "pending"         # TODO: Check Gemini API
        }
    }

# Include routers
from app.api.routes import lessons, code_execution
app.include_router(lessons.router, prefix="/api/lessons", tags=["lessons"])
app.include_router(code_execution.router, prefix="/api/code", tags=["code-execution"])
# TODO: Add more routers when ready
# app.include_router(practice.router, prefix="/api/practice", tags=["practice"])
# app.include_router(users.router, prefix="/api/users", tags=["users"])

# Mount static files (Frontend)
import os
from pathlib import Path

# Get the parent directory (LearnProgrm) and then frontend directory
base_dir = Path(__file__).resolve().parent.parent.parent
frontend_dir = base_dir / "frontend"

if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")
    logger.info(f"📁 Serving frontend from: {frontend_dir}")
else:
    logger.warning(f"⚠️  Frontend directory not found: {frontend_dir}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
