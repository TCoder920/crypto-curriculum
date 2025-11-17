"""Application configuration settings"""
from pydantic_settings import BaseSettings
from typing import List
from pydantic import field_validator, Field
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "Crypto Curriculum Platform"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # Database
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/crypto_curriculum"
    DATABASE_ECHO: bool = False
    
    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production-min-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS (stored as string, parsed to list)
    CORS_ORIGINS_STR: str = "http://localhost:5173,http://localhost:3000"
    CORS_ALLOW_CREDENTIALS: bool = True
    
    @property
    def CORS_ORIGINS(self) -> List[str]:
        """Parse CORS_ORIGINS from comma-separated string"""
        return [origin.strip() for origin in self.CORS_ORIGINS_STR.split(',')]
    
    # LLM Configuration (optional for Phase 2)
    DEFAULT_LLM_PROVIDER: str = "anthropic"
    DEFAULT_LLM_MODEL: str = "claude-3-5-sonnet-20241022"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 2000
    ANTHROPIC_API_KEY: str | None = None
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    
    # OpenAI Assistants API Configuration
    OPENAI_API_KEY: str = Field(default="", env="OPENAI_API_KEY")  # Required for AI chat
    BRAVE_API_KEY: str = Field(default="", env="BRAVE_API_KEY")  # Optional, for web search
    OPENAI_ASSISTANT_ID: str = Field(default="", env="OPENAI_ASSISTANT_ID")  # Optional, global fallback assistant
    
    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_FILE_TYPES: str = "jpg,jpeg,png,pdf"
    DOCUMENT_ALLOWED_TYPES: str = "pdf,docx,txt,jpg,jpeg,png,gif,webp"
    DOCUMENT_STORAGE_PATH: str = "storage/documents"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields in .env


# Create settings instance - will use environment variables or .env file
# If .env file has issues, environment variables take precedence
try:
    settings = Settings()
except Exception as e:
    # If loading fails, try with minimal required env vars
    import os
    os.environ.setdefault("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/crypto_curriculum")
    os.environ.setdefault("SECRET_KEY", "dev-secret-key-change-in-production")
    settings = Settings()

