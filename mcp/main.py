# Libs
from mcp.server import MCPServer  # MCP Server

# Application
from tools import weather, home, led, relay, pico  # Tools

# Create MCP Server
mcp = MCPServer(
    title="Rachel Assistant MCP Server",
    version="0.1.0",
)

weather.register(mcp)
home.register(mcp)
led.register(mcp)
relay.register(mcp)
pico.register(mcp)

# Runs:
## STDIO
### uv run mcp run main.py --transport stdio
## HTTP
### uv run mcp run main.py --transport streamable-http
