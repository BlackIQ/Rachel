# Libs
from fastmcp.tools import tool  # FastMCP Tool

import requests  # Requests
from requests.exceptions import RequestException  # Requests Exception

# Application
from core.settings import settings  # Core: Settings
from schemas.response import ToolResult  # Schema: Tool Result


class Pico:
    @tool(
        name="get_pico_resources",
        title="Get Pico Resources",
        description="Get Raspberry Pi Pico memory information",
    )
    def get_pico_resources(self) -> dict:
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


pico = Pico()
