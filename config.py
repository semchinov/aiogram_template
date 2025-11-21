"""
Configuration module for the bot.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional


class Settings(BaseSettings):
    """Bot configuration settings loaded from environment variables."""
    
    # Bot settings
    bot_token: str
    
    # Admin settings
    admins: str = ""
    
    # Database settings
    database_url: str = "sqlite+aiosqlite:///./bot.db"
    
    # Logging settings
    log_level: str = "INFO"
    
    # Rate limit settings
    rate_limit: float = 0.5
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @property
    def admin_ids(self) -> List[int]:
        """Parse admin IDs from comma-separated string."""
        if not self.admins:
            return []
        
        result = []
        for admin_id in self.admins.split(","):
            admin_id = admin_id.strip()
            if admin_id:
                try:
                    result.append(int(admin_id))
                except ValueError:
                    # Skip invalid admin IDs
                    continue
        return result


def get_settings() -> Settings:
    """
    Get settings instance with proper error handling.
    """
    try:
        return Settings()
    except Exception as e:
        print(f"Error loading settings: {e}")
        print("Please make sure you have created a .env file with BOT_TOKEN set.")
        print("You can copy .env.example to .env and fill in your values.")
        raise


# Create a global settings instance
settings = get_settings()
