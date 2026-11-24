package config

import (
	"os"

	"github.com/BlackIQ/Rachel/backend/internal/enums"
)

type Config struct {
	Environment enums.AppEnv
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

	config = &Config{
		Environment: env,
	}

	return nil
}

func GetConfig() *Config {
	return config
}
