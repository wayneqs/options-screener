"""Configuration management."""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration."""
    
    def __init__(self):
        # API Configuration
        self.api_key: str = os.getenv("FMP_API_KEY", "")
        self.api_base_url: str = os.getenv("FMP_API_BASE_URL", "https://api.example.com/v1")
        self.api_timeout: int = int(os.getenv("API_TIMEOUT", "30"))
        
        # Environment
        self.environment: str = os.getenv("ENVIRONMENT", "development")
        self.debug: bool = os.getenv("DEBUG", "false").lower() == "true"
        
        # Project paths
        self.project_root = Path(__file__).parent.parent.parent
        self.data_dir = self.project_root / "data"
        
    def validate(self) -> bool:
        """Validate required configuration."""
        if not self.api_key:
            raise ValueError("FMP_API_KEY is required. Please set it in your .env file.")
        return True
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment == "development"

# Global config instance
config = Config()