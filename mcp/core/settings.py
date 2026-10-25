# Libs
from pydantic_settings import BaseSettings, SettingsConfigDict  # Pydantic Settings


# Settings
class Settings(BaseSettings):
    # Hardware (Raspberry Pi Pico 2 W)
    PICO_IP: str = ""
    PICO_SECRET: str = ""

    # Weather API
    WEATHER_APIKEY: str = ""

    model_config = SettingsConfigDict(env_file=".env")


# Run the settings
settings = Settings()
