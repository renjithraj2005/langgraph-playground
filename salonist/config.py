from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr
from functools import lru_cache
from pathlib import Path
import os


class Settings(BaseSettings):
    """Application settings."""
    
    # Python Settings
    PYTHONDONTWRITEBYTECODE: str = Field(default="1", description="Disable Python bytecode generation")
    
    # Application Settings
    APP_NAME: str = Field(default="Salonist", description="Application name")
    APP_ENV: str = Field(default="development", description="Application environment (development/production)")
    DEBUG: bool = Field(default=True, description="Debug mode")
    
    # Server Settings
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    
    # Database Settings
    DATABASE_URL: Optional[str] = Field(default=None, description="Database connection URL")
    
    # Security Settings
    SECRET_KEY: SecretStr = SecretStr(os.urandom(24).hex())
    
    # API Keys
    ANTHROPIC_API_KEY: str = Field(default="", description="Anthropic API key")
    TAVILY_API_KEY: Optional[SecretStr] = None
    
    # Database
    SQLALCHEMY_DATABASE_URI: str = Field(default="sqlite:///salonist.db", description="Database connection URL")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = Field(default=False, description="Track modifications")
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields like FLASK_APP


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance
    """
    return Settings()


# Create a global settings instance
settings = get_settings() 