# Rachel MCP Server

MCP server that exposes Rachel's tools (home sensors, LEDs, relays, Pico resources, and weather) over **Streamable HTTP**.

The backend (and any other MCP client) can connect to this server instead of calling the hardware tools directly.

## Techs

- **Python**: Programming language
- **MCP**: Model Context Protocol
- **UV**: Dependency management
- **Requests**: HTTP client for Pico and WeatherAPI

## Tools

| Tool                   | Description                                   |
| ---------------------- | --------------------------------------------- |
| `get_weather`          | Current weather for a city (WeatherAPI)       |
| `get_home_temperature` | Temperature & humidity from DHT11 on the Pico |
| `get_pico_resources`   | Free / allocated RAM on the Pico              |
| `turn_led_on`          | Turn a specific LED on                        |
| `turn_led_off`         | Turn a specific LED off                       |
| `turn_relay_on`        | Turn a specific relay on                      |
| `turn_relay_off`       | Turn a specific relay off                     |

Valid LEDs: `white`, `green`, `red`, `blue`  
Valid relays: `library`, `bedroom`, `living_room`, `kitchen`, `r1`, `r2`, `r3`, `r4`

## Setup

First go inside directory:

```bash
cd mcp
```

Sync dependencies:

```bash
uv sync
```

### Configure `.env`

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Then edit it:

```env
PICO_IP="http://192.168.1.50"
PICO_SECRET="your-strong-token"
WEATHER_APIKEY="your-weatherapi-key"
```

### Run

```bash
uv run main.py
```

- Server: `http://127.0.0.1:8080`
- Transport: Streamable HTTP

Any MCP client can now connect to this endpoint and use the tools above.
