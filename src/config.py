"""
Configuration module for the agentic AI application.
"""
import os
from typing import Optional
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    openai_api_key: Optional[str] = None
    host: str = "localhost"
    port: int = 8000
    
    # Database Configuration
    database_url: str = "sqlite:///data/agent.db"
    
    # Logging Configuration
    log_level: str = "INFO"
    
    # Agent Configuration
    model_name: str = "gpt-4-turbo-preview"
    max_conversation_history: int = 50
    max_tool_results_length: int = 2000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Global settings instance
settings = Settings()
