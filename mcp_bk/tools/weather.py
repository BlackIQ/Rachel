# Libs
from fastmcp.tools import tool  # FastMCP Tool

import requests  # Requests
from requests.exceptions import RequestException  # Requests Exception

# Application
from core.settings import settings  # Core: Settings
from schemas.response import ToolResult  # Schema: Tool Result

VALID_LEDS = {
    "white",
    "green",
    "red",
    "blue",
}


class Weather:
    @tool(
        name="get_weather",
        title="Get Weather",
        description="Get the current weather information for a city",
    )
    def get_weather(self, city: str) -> dict:
        """Get the current weather information for a city.

        Args:
            city: The name of the city

        Returns:
            ToolResult as dict. On success, data is the WeatherAPI payload.

            On failure, error may be:
                - missing_api_key
                - weather_api_error
                - network_error
                - invalid_response
        """

        if not settings.WEATHER_APIKEY:
            return ToolResult(
                success=False,
                error="missing_api_key",
                message="Weather API key is not set in .env",
            ).to_json()

        try:
            response = requests.get(
                "https://api.weatherapi.com/v1/current.json",
                params={
                    "q": city,
                    "key": settings.WEATHER_APIKEY,
                },
                timeout=8,
            )

            try:
                data = response.json()
            except ValueError:
                return ToolResult(
                    success=False,
                    error="invalid_response",
                    message="WeatherAPI returned invalid JSON",
                ).to_json()

            if not response.ok:
                error_msg = data.get("error", {}).get(
                    "message", "Unknown weather API error"
                )
                return ToolResult(
                    success=False,
                    error="weather_api_error",
                    message=error_msg,
                ).to_json()

            return ToolResult(
                success=True,
                message=f"Weather for {city}",
                data=data,
            ).to_json()

        except RequestException:
            return ToolResult(
                success=False,
                error="network_error",
                message="Could not reach WeatherAPI. Check your internet connection.",
            ).to_json()


weather = Weather()
