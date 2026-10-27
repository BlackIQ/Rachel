# Libs
from fastmcp import FastMCP  # FastMCP

# Application
from tools.home import home  # Tools: Home
from tools.pico import pico  # Tools: Pico
from tools.weather import weather  # Tools: Weather
from tools.led import led  # Tools: LED
from tools.relay import relay  # Tools: Relay

# Create MCP Server
app = FastMCP(
    name="Rachel Assistant MCP Server",
    version="0.1.0",
    website_url="rachel.amirhossein.info",
)

app.add_tool(home.get_home_temperature)
app.add_tool(pico.get_pico_resources)
app.add_tool(weather.get_weather)
app.add_tool(led.turn_led_on)
app.add_tool(led.turn_led_off)
app.add_tool(relay.turn_relay_on)
app.add_tool(relay.turn_relay_off)

# How to run
## STDIO
### uv run fastmcp run main.py:app --transport stdio
## HTTP
### uv run fastmcp run main.py:app --transport http
