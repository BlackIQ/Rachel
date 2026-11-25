package inits

import (
	"errors"

	"github.com/BlackIQ/Rachel/internal/ollama"
)

func InitOllama() (err error) {
	if err := ollama.InitOllama(); err != nil {
		return errors.New("[ollama.go] Can't init Ollama: " + err.Error())
	}

	return nil
}
