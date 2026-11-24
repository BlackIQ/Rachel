package agent

import (
	"context"
	"errors"

	"github.com/ollama/ollama/api"

	"github.com/BlackIQ/Rachel/backend/internal/enums"
	"github.com/BlackIQ/Rachel/backend/internal/models"
)

func Run(history []models.Message) (message *models.Message, err error) {
	stream := false
	think := &api.ThinkValue{
		Value: false,
	}

	var ollamaResp api.ChatResponse

	ctx := context.Background()

	messages := []api.Message{}

	for _, m := range history {
		messages = append(messages, api.Message{
			Role:    string(m.Role),
			Content: m.Content,
		})
	}

	client, err := api.ClientFromEnvironment()

	if err != nil {
		return nil, errors.New("Could not connect to Ollama:" + err.Error())
	}

	err = client.Heartbeat(ctx)

	if err != nil {
		return nil, errors.New("Ollama is not available:" + err.Error())
	}

	req := &api.ChatRequest{
		Model:    "rachel:test-1",
		Messages: messages,
		Stream:   &stream,
		Think:    think,
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
