# Rachel Firmware

**MicroPython firmware** for **Raspberry Pi Pico 2 W**. Wi‑Fi, DHT11, LEDs, I2C LCD, and a small HTTP API with **Microdot**.

The FastAPI backend calls this device for temperature/humidity, LED control, and memory stats and other stuff.

## Techs

- **Python**: Programming language
- **MicroPython**: Runtime
- **Raspberry Pi Pico 2 W**: Hardware
- **Microdot**: Flask like for MicroPython

## Hardware parts

Things I used for this project:

| Part                        | Notes                                               |
| --------------------------- | --------------------------------------------------- |
| Raspberry Pi Pico 2 W       | Hardware having Wi-Fi thanks to Raspberry Pi        |
| DS3231 RTC                  | Clock module                                        |
| DHT11                       | Temperature and humidity sensor                     |
| Liquid crystal 16×2 I2C LCD | Just to see some stuff in LCD like IP and RAM usage |
| LEDs                        | White, Green, Red, Blue                             |
| Relays                      | Library, Bedroom, Living room, Kitchen              |

## Pins

A simple table to remember what is connected to what:

| Pin            | Details            |
| -------------- | ------------------ |
| GP0 - I2C0 SDA | SDA I2C Bus        |
| GP1 - I2C0 DSA | SCL I2C Bus        |
| GP6            | Relay: Library     |
| GP7            | Relay: Bedroom     |
| GP8            | Relay: Living room |
| GP9            | Relay: Kitchen     |
| GP10           | Relay: R1 (-)      |
| GP11           | Relay: R2 (-)      |
| GP12           | Relay: R3 (-)      |
| GP13           | Relay: Nightlight  |
| GP16           | LED: White         |
| GP17           | LED: Green         |
| GP18           | LED: Red           |
| GP19           | LED: Blue          |
| GP22           | DHT11 Sensor Data  |
| GP26 - ADC0    | Photocell resistor |

## Files

Let's take a look what is inside it:

- `main.py`: App entry
- `config.py`: Configs. Wi-Fi SSID & PASSWD, Secret
- `microdot`: Bundled Microdot server directory (Flask like framework)
- `picozero`: Bundled Pico Zero server directory (RPI Pico things)
- `lcd`: Bundled LCD server directory (LCD Display)
- `urtc`: Bundled URTC server directory (Real time clock)

## Setup

1. Flash **MicroPython** for Pico 2 W.
2. Edit `config.py`:

```python
SSID = "wifi-name"
PASSWORD = "wifi-password"
TOKEN = "Your token"
```

3. Copy all files in this folder to the Pico with Thonny.
4. Run `main.py` (or set it as `main.py` so it starts on boot).
5. Read the IP from the LCD

## API endpoints

Base URL: `http://<pico-ip>/`

| Method | Path                     | Description                                |
| ------ | ------------------------ | ------------------------------------------ |
| GET    | `/`                      | Welcome JSON                               |
| GET    | `/api/temperature`       | Get `temperature` and `humidity`           |
| POST   | `/api/leds/<name>/on`    | Turn LED on. Pass `name` as LED name       |
| POST   | `/api/leds/<name>/off`   | Turn LED off. Pass `name` as LED name      |
| POST   | `/api/relays/<name>/on`  | Turn relay on. Pass `name` as relay name   |
| POST   | `/api/relays/<name>/off` | Turn relay off. Pass `name` as relays name |
| GET    | `/api/system/memory`     | Get `free` and `allocated`                 |

## Runtime

- Connects to network; Onboard LED blinks until connected, then stays on.
- Background task samples DHT11 about every **2 seconds**.
- LCD cycles status screens (ready, credit, IP, RAM).
- HTTP server listens on **port 80**.
