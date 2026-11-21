package config

import (
	"os"

	"github.com/joho/godotenv"
)

type Config struct {
	PicoIP        string
	PicoSecret    string
	WeatherAPIKey string
}

func Load() *Config {
	_ = godotenv.Load()

	return &Config{
		PicoIP:        getEnv("PICO_IP", ""),
		PicoSecret:    getEnv("PICO_SECRET", ""),
		WeatherAPIKey: getEnv("WEATHER_APIKEY", ""),
	}
}

func getEnv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}

	return fallback
}
