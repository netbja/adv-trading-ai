"""
🔧 CONFIGURATION - TRADING AI ETF BACKEND
Settings et configuration de l'application
"""

from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Configuration de l'application"""
    
    # App Configuration
    APP_NAME: str = "Trading AI ETF Backend"
    ENVIRONMENT: str = "development"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    LOG_LEVEL: str = "DEBUG"
    
    # Database
    DATABASE_URL: str = "postgresql://trader:TradingDB2025!@postgres:5432/trading_ai"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    
    # AI APIs
    OPENAI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    
    # Broker APIs
    ALPACA_API_KEY: str = ""
    ALPACA_SECRET_KEY: str = ""
    ALPACA_BASE_URL: str = "https://paper-api.alpaca.markets"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:80",
        "http://localhost:8080",
        "http://frontend:3000"
    ]
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Instance globale des settings
settings = Settings() 