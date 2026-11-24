package inits

import (
	"errors"

	"github.com/joho/godotenv"

	"github.com/BlackIQ/Rachel/backend/internal/config"
)

func InitDotenv() (err error) {
	if err := godotenv.Load(); err != nil {
		return errors.New("[dotenv.go] Can't load dotenv: " + err.Error())
	}

	if err := config.InitConfig(); err != nil {
		return errors.New("[dotenv.go] Can't load config: " + err.Error())
	}

	return nil
}
