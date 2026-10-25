# Libs
from mcp.server import MCPServer  # MCP Server

import requests  # Requests
from requests.exceptions import RequestException  # Requests Exception

# Application
from core.settings import settings  # Core: Settings
from schemas.response import ToolResult

# Create MCP Server
mcp = MCPServer(
    title="Rachel Assistant MCP Server",
    version="0.1.0",
)


VALID_LEDS = {
    "white",
    "green",
    "red",
    "blue",
}

VALID_RELAYS = {
    "library",
    "bedroom",
    "living_room",
    "kitchen",
    "r1",
    "r2",
    "r3",
    "r4",
}


# Weather Tool
@mcp.tool(
    name="get_weather",
    title="Get Weather",
    description="Get the current weather information for a city",
)
def get_weather(city: str) -> dict:
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


@mcp.tool(
    name="get_home_temperature",
    title="Get Home Temperature",
    description="Get the current home temperature information",
)
def get_home_temperature() -> dict:
    """Get the current home temperature information.

    Returns:
        ToolResult as dict. On success, data includes:
            - temperature: home temperature
            - humidity: home humidity

        On failure, error may be:
            - auth_failed: Pico rejected the token
            - pico_unreachable: network / device offline
            - pico_error: other HTTP error from Pico
            - invalid_response: non-JSON body
    """

    try:
        headers = {
            "Authorization": f"Bearer {settings.PICO_SECRET}",
        }

        response = requests.get(
            f"{settings.PICO_IP}/api/temperature",
            headers=headers,
            timeout=5,
        )

        try:
            data = response.json()
        except ValueError:
            return ToolResult(
                success=False,
                error="invalid_response",
                message="Pico returned invalid JSON",
            ).to_json()

        if response.status_code == 401:
            return ToolResult(
                success=False,
                error="auth_failed",
                message="Authentication failed. Check PICO_SECRET and Pico TOKEN.",
            ).to_json()

        if not response.ok:
            return ToolResult(
                success=False,
                error="pico_error",
                message=data.get("message", "Pico error"),
            ).to_json()

        return ToolResult(
            success=True,
            message="Home sensor reading",
            data={
                "temperature": data.get("temperature"),
                "humidity": data.get("humidity"),
            },
        ).to_json()

    except RequestException:
        return ToolResult(
            success=False,
            error="pico_unreachable",
            message="Could not reach the Pico device. Check power and network.",
        ).to_json()


@mcp.tool(
    name="turn_led_on",
    title="Turn LED On",
    description="Turn on a specific LED on the Rachel Pico device",
)
def turn_led_on(name: str) -> dict:
    """Turn on a specific LED on the Rachel Pico device.

    Args:
        name: LED name. One of: "green", "red", "blue", "white".

    Returns:
        ToolResult as dict.

        On failure, error may be:
            - unknown_led
            - auth_failed
            - pico_unreachable
            - pico_error
            - invalid_response
    """

    if name not in VALID_LEDS:
        return ToolResult(
            success=False,
            error="unknown_led",
            message=f"Unknown LED: {name}",
        ).to_json()

    try:
        headers = {
            "Authorization": f"Bearer {settings.PICO_SECRET}",
        }

        response = requests.post(
            f"{settings.PICO_IP}/api/leds/{name}/on",
            headers=headers,
            timeout=5,
        )

        try:
            data = response.json()
        except ValueError:
            return ToolResult(
                success=False,
                error="invalid_response",
                message="Pico returned invalid JSON",
            ).to_json()

        if response.status_code == 401:
            return ToolResult(
                success=False,
                error="auth_failed",
                message="Authentication failed. Check PICO_SECRET and Pico TOKEN.",
            ).to_json()

        if not response.ok:
            return ToolResult(
                success=False,
                error="pico_error",
                message=data.get("message", "Pico error"),
            ).to_json()

        return ToolResult(
            success=True,
            message=data.get("message", f"LED {name} is now on"),
        ).to_json()

    except RequestException:
        return ToolResult(
            success=False,
            error="pico_unreachable",
            message="Could not reach the Pico device. Check power and network.",
        ).to_json()


@mcp.tool(
    name="turn_led_off",
    title="Turn LED off",
    description="Turn off a specific LED on the Rachel Pico device",
)
def turn_led_off(name: str) -> dict:
    """Turn off a specific LED on the Rachel Pico device.

    Args:
        name: LED name. One of: "green", "red", "blue", "white".

    Returns:
        ToolResult as dict.

        On failure, error may be:
            - unknown_led
            - auth_failed
            - pico_unreachable
            - pico_error
            - invalid_response
    """

    if name not in VALID_LEDS:
        return ToolResult(
            success=False,
            error="unknown_led",
            message=f"Unknown LED: {name}",
        ).to_json()

    try:
        headers = {
            "Authorization": f"Bearer {settings.PICO_SECRET}",
        }

        response = requests.post(
            f"{settings.PICO_IP}/api/leds/{name}/off",
            headers=headers,
            timeout=5,
        )

        try:
            data = response.json()
        except ValueError:
            return ToolResult(
                success=False,
                error="invalid_response",
                message="Pico returned invalid JSON",
            ).to_json()

        if response.status_code == 401:
            return ToolResult(
                success=False,
                error="auth_failed",
                message="Authentication failed. Check PICO_SECRET and Pico TOKEN.",
            ).to_json()

        if not response.ok:
            return ToolResult(
                success=False,
                error="pico_error",
                message=data.get("message", "Pico error"),
            ).to_json()

        return ToolResult(
            success=True,
            message=data.get("message", f"LED {name} is now off"),
        ).to_json()

    except RequestException:
        return ToolResult(
            success=False,
            error="pico_unreachable",
            message="Could not reach the Pico device. Check power and network.",
        ).to_json()


@mcp.tool(
    name="turn_relay_on",
    title="Turn Relay On",
    description="Turn on a specific relay on the Rachel Pico device",
)
def turn_relay_on(name: str) -> dict:
    """Turn on a specific relay on the Rachel Pico device.

    Args:
        name: Relay name. One of: "library", "bedroom", "living_room", "kitchen", "r1", "r2", "r3", "r4".

    Returns:
        ToolResult as dict.

        On failure, error may be:
            - unknown_relay
            - auth_failed
            - pico_unreachable
            - pico_error
            - invalid_response
    """

    if name not in VALID_RELAYS:
        return ToolResult(
            success=False,
            error="unknown_relay",
            message=f"Unknown relay: {name}",
        ).to_json()

    try:
        headers = {
            "Authorization": f"Bearer {settings.PICO_SECRET}",
        }

        response = requests.post(
            f"{settings.PICO_IP}/api/relays/{name}/on",
            headers=headers,
            timeout=5,
        )

        try:
            data = response.json()
        except ValueError:
            return ToolResult(
                success=False,
                error="invalid_response",
                message="Pico returned invalid JSON",
            ).to_json()

        if response.status_code == 401:
            return ToolResult(
                success=False,
                error="auth_failed",
                message="Authentication failed. Check PICO_SECRET and Pico TOKEN.",
            ).to_json()

        if not response.ok:
            return ToolResult(
                success=False,
                error="pico_error",
                message=data.get("message", "Pico error"),
            ).to_json()

        return ToolResult(
            success=True,
            message=data.get("message", f"Relay {name} is now on"),
        ).to_json()

    except RequestException:
        return ToolResult(
            success=False,
            error="pico_unreachable",
            message="Could not reach the Pico device. Check power and network.",
        ).to_json()


@mcp.tool(
    name="turn_relay_off",
    title="Turn Relay Off",
    description="Turn off a specific relay on the Rachel Pico device",
)
def turn_relay_off(name: str) -> dict:
    """Turn off a specific relay on the Rachel Pico device.

    Args:
        name: Relay name. One of: "library", "bedroom", "living_room", "kitchen", "r1", "r2", "r3", "r4".

    Returns:
        ToolResult as dict.

        On failure, error may be:
            - unknown_relay
            - auth_failed
            - pico_unreachable
            - pico_error
            - invalid_response
    """

    if name not in VALID_RELAYS:
        return ToolResult(
            success=False,
            error="unknown_relay",
            message=f"Unknown relay: {name}",
        ).to_json()

    try:
        headers = {
            "Authorization": f"Bearer {settings.PICO_SECRET}",
        }

        response = requests.post(
            f"{settings.PICO_IP}/api/relays/{name}/off",
            headers=headers,
            timeout=5,
        )

        try:
            data = response.json()
        except ValueError:
            return ToolResult(
                success=False,
                error="invalid_response",
                message="Pico returned invalid JSON",
            ).to_json()

        if response.status_code == 401:
            return ToolResult(
                success=False,
                error="auth_failed",
                message="Authentication failed. Check PICO_SECRET and Pico TOKEN.",
            ).to_json()

        if not response.ok:
            return ToolResult(
                success=False,
                error="pico_error",
                message=data.get("message", "Pico error"),
            ).to_json()

        return ToolResult(
            success=True,
            message=data.get("message", f"Relay {name} is now off"),
        ).to_json()

    except RequestException:
        return ToolResult(
            success=False,
            error="pico_unreachable",
            message="Could not reach the Pico device. Check power and network.",
        ).to_json()


@mcp.tool(
    name="get_pico_resources",
    title="Get Pico Resources",
    description="Get Raspberry Pi Pico memory information",
)
def get_pico_resources() -> dict:
    """
    Get Raspberry Pi Pico memory information

    Returns:
        ToolResult as dict. On success, data includes:
            - free: free memory
            - allocated: allocated memory

        On failure, error may be:
            - auth_failed
            - pico_unreachable
            - pico_error
            - invalid_response
    """

    try:
        headers = {
            "Authorization": f"Bearer {settings.PICO_SECRET}",
        }

        response = requests.get(
            f"{settings.PICO_IP}/api/system/memory",
            headers=headers,
            timeout=5,
        )

        try:
            data = response.json()
        except ValueError:
            return ToolResult(
                success=False,
                error="invalid_response",
                message="Pico returned invalid JSON",
            ).to_json()

        if response.status_code == 401:
            return ToolResult(
                success=False,
                error="auth_failed",
                message="Authentication failed. Check PICO_SECRET and Pico TOKEN.",
            ).to_json()

        if not response.ok:
            return ToolResult(
                success=False,
                error="pico_error",
                message=data.get("message", "Pico error"),
            ).to_json()

        return ToolResult(
            success=True,
            message="Pico memory reading",
            data={
                "free": data.get("free"),
                "allocated": data.get("allocated"),
            },
        ).to_json()

    except RequestException:
        return ToolResult(
            success=False,
            error="pico_unreachable",
            message="Could not reach the Pico device. Check power and network.",
        ).to_json()


def main():
    mcp.run(transport="streamable-http", port=8080)


if __name__ == "__main__":
    main()
