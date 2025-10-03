"""
Configuration Management
Loads environment variables and application settings
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    APP_NAME: str = "AI Learn Programming Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Google Gemini AI
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # Database
    DATABASE_URL: str
    DB_ECHO: bool = False

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600

    # Code Execution
    SANDBOX_TIMEOUT: int = 30
    MAX_CODE_LENGTH: int = 10000
    ALLOWED_LANGUAGES: str = "python,javascript,java,cpp"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    class Config:
        env_file = ".env"
        case_sensitive = True


def get_settings() -> Settings:
    """
    Get settings instance
    Note: Removed lru_cache for development to allow .env changes to reload
    """
    return Settings()


# Global settings instance
settings = get_settings()
