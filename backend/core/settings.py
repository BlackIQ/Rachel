# Libs
from pydantic_settings import BaseSettings, SettingsConfigDict  # Pydantic Settings


# Settings
class Settings(BaseSettings):
    # Model
    MODEL: str = "rachel-1.4:4b"

    # Database
    POSTGRESQL_URL: str = ""

    # MCP Integration: GitHub
    MCP_GITHUB_TOKEN: str = ""

    model_config = SettingsConfigDict(env_file=".env")


# Run the settings
settings = Settings()
