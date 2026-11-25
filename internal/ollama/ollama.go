package ollama

import (
	"errors"

	"github.com/ollama/ollama/api"
)

var Client *api.Client

func InitOllama() (err error) {
	client, err := api.ClientFromEnvironment()

	if err != nil {
		return errors.New("[ollama.go] Ollama Connection: " + err.Error())
	}

	Client = client

	return nil
}

func GetOllama() *api.Client {
	return Client
}
