package agent

import (
	"context"
	"errors"
	"time"

	"github.com/ollama/ollama/api"

	"github.com/BlackIQ/Rachel/backend/internal/config"
	"github.com/BlackIQ/Rachel/backend/internal/enums"
	"github.com/BlackIQ/Rachel/backend/internal/models"
	"github.com/BlackIQ/Rachel/backend/internal/ollama"
)

func Run(parent context.Context, history []models.Message) (message *models.Message, err error) {
	cfg := config.GetConfig()

	client := ollama.GetOllama()

	ollamaConfig := cfg.OllamaConfig

	var ollamaResp api.ChatResponse

	ctx, cancel := context.WithTimeout(
		parent,
		2*time.Minute,
	)
	defer cancel()

	messages := []api.Message{}

	for _, m := range history {
		messages = append(messages, api.Message{
			Role:    string(m.Role),
			Content: m.Content,
		})
	}

	err = client.Heartbeat(ctx)

	if err != nil {
		return nil, errors.New("Ollama is not available:" + err.Error())
	}

	req := &api.ChatRequest{
		Model:    ollamaConfig.Model,
		Stream:   &ollamaConfig.Stream,
		Think:    &ollamaConfig.Think,
		Messages: messages,
	}

	res := func(resp api.ChatResponse) error {
		ollamaResp = resp

		return nil
	}

	err = client.Chat(ctx, req, res)

	if err != nil {
		return nil, errors.New("Error in Ollama Chat:" + err.Error())
	}

	assistantMsg := models.Message{
		Content: ollamaResp.Message.Content,
		Role:    enums.Assistant,
	}

	return &assistantMsg, nil
}
