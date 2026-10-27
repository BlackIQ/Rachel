# Libs
from fastmcp.tools import tool  # FastMCP Tool

import requests  # Requests
from requests.exceptions import RequestException  # Requests Exception

# Application
from core.settings import settings  # Core: Settings
from schemas.response import ToolResult  # Schema: Tool Result

VALID_RELAYS = {
    "library",
    "bedroom",
    "living_room",
    "kitchen",
    "r1",
    "r2",
    "r3",
}


class Relay:
    @tool(
        name="turn_relay_on",
        title="Turn Relay On",
        description="Turn on a specific relay on the Rachel Pico device",
    )
    def turn_relay_on(self, name: str) -> dict:
        """Turn on a specific relay on the Rachel Pico device.

        Args:
            name: Relay name. One of: "library", "bedroom", "living_room", "kitchen", "r1", "r2", "r3".

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

    @tool(
        name="turn_relay_off",
        title="Turn Relay Off",
        description="Turn off a specific relay on the Rachel Pico device",
    )
    def turn_relay_off(self, name: str) -> dict:
        """Turn off a specific relay on the Rachel Pico device.

        Args:
            name: Relay name. One of: "library", "bedroom", "living_room", "kitchen", "r1", "r2", "r3".

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


relay = Relay()
