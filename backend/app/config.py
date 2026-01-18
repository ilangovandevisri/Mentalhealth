"""
Configuration settings for the backend
"""
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/mental_health_db"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # ML Model paths
    ML_MODEL_PATH: str = "./ml/models/trained_models"
    
    # RAG configuration
    RAG_ENABLED: bool = True
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    # API Settings
    API_TITLE: str = "Mental Health Risk Detection API"
    API_VERSION: str = "1.0.0"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
