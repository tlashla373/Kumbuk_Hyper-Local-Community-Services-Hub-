"""
Configuration settings for the application
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Kumbuk AI Agent System"
    VERSION: str = "1.0.0"
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    # Firebase Configuration (mock for now)
    FIREBASE_PROJECT_ID: Optional[str] = None
    FIREBASE_API_KEY: Optional[str] = None
    
    # Neo4j Configuration (for future use)
    NEO4J_URI: Optional[str] = None
    NEO4J_USER: Optional[str] = None
    NEO4J_PASSWORD: Optional[str] = None
    
    # Vertex AI Configuration (for future use)
    GOOGLE_CLOUD_PROJECT: Optional[str] = None
    VERTEX_AI_LOCATION: str = "us-central1"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
