package config

import (
	"os"

	"github.com/ollama/ollama/api"

	"github.com/BlackIQ/Rachel/backend/internal/enums"
)

type Config struct {
	Environment enums.AppEnv
	OllamaConfig
}

type OllamaConfig struct {
	Model  string
	Stream bool
	Think  api.ThinkValue
}

var config *Config

func InitConfig() error {
	environment := os.Getenv("APP_ENV")

	if environment == "" {
		environment = string(enums.Production)
	} else {
		environment = string(enums.Development)
	}

	env := enums.AppEnv(environment)

	ollamaConfig := OllamaConfig{
		Model:  "rachel:test-1",
		Stream: false,
		Think: api.ThinkValue{
			Value: true,
		},
	}

	config = &Config{
		Environment:  env,
		OllamaConfig: ollamaConfig,
	}

	return nil
}

func GetConfig() *Config {
	return config
}
