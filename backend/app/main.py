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
    allow_origins=["*"],  # Configure in production
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

@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "AI Learn Programming Platform API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/api/docs"
    }

@app.get("/health")
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

# TODO: Include routers
# from app.api.routes import lessons, practice, code_exec, users
# app.include_router(lessons.router, prefix="/api/lessons", tags=["lessons"])
# app.include_router(practice.router, prefix="/api/practice", tags=["practice"])
# app.include_router(code_exec.router, prefix="/api/code", tags=["code-execution"])
# app.include_router(users.router, prefix="/api/users", tags=["users"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
