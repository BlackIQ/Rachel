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


# def main():
#     mcp.run(transport="streamable-http", port=8080)


# if __name__ == "__main__":
#     main()
