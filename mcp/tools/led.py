# Libs
from fastmcp.tools import tool  # FastMCP Tool
from pydantic import Field  # Pydantic
import requests  # Requests
from requests.exceptions import RequestException  # Requests Exception

# Application
from core.settings import settings  # Core: Settings
from schemas.response import ToolResult  # Schema: Tool Result
from enums.led import LEDName  # Enums: LED

VALID_LEDS = {
    "white",
    "green",
    "red",
    "blue",
}


class LED:
    @tool(
        name="turn_led_on",
        title="Turn LED On",
        description=(
            "Turn on a specific LED connected to the Raspberry Pi Pico."
            "Use this when the user asks to turn on a light/LED (white, green, red or blue)."
            "Valid names: white, green, red, blue."
        ),
    )
    def turn_led_on(
        self,
        name: LEDName = Field(
            ...,
            title="LED Name",
            description="Which LED to turn on. Must be one of: white, green, red, blue.",
        ),
    ) -> dict:
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

    @tool(
        name="turn_led_off",
        title="Turn LED Off",
        description=(
            "Turn off a specific LED connected to the Raspberry Pi Pico."
            "Use this when the user asks to turn off a light/LED (white, green, red or blue)."
            "Valid names: white, green, red, blue."
        ),
    )
    def turn_led_off(
        self,
        name: LEDName = Field(
            ...,
            title="LED Name",
            description="Which LED to turn off. Must be one of: white, green, red, blue.",
        ),
    ) -> dict:
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


led = LED()
