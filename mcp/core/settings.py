# Libs
from pydantic_settings import BaseSettings, SettingsConfigDict  # Pydantic Settings


# Settings
class Settings(BaseSettings):
    # Weather API
    WEATHER_APIKEY: str = ""

    model_config = SettingsConfigDict(env_file=".env")


# Run the settings
settings = Settings()
