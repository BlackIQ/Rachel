package services

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/google/uuid"

	"github.com/BlackIQ/Rachel/backend/internal/enums"
	"github.com/BlackIQ/Rachel/backend/internal/models"
)

const (
	ollamaBaseURL = "http://localhost:11434"
	modelName     = "kimi-k3:cloud"
)

type MessageInput struct {
	Role     enums.MessageRole
	Content  string
	ToolName *string
}

type ollamaMessage struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

type ollamaChatRequest struct {
	Model    string          `json:"model"`
	Messages []ollamaMessage `json:"messages"`
	Stream   bool            `json:"stream"`
}

type ollamaChatResponse struct {
	Message ollamaMessage `json:"message"`
}

func Run(history []MessageInput) ([]models.Message, error) {
	if modelName == "" {
		return nil, fmt.Errorf("model name is empty")
	}

	messages := make([]ollamaMessage, 0, len(history))
	for _, msg := range history {
		if msg.Role == enums.Tool {
			continue
		}
		role := string(msg.Role)
		messages = append(messages, ollamaMessage{
			Role:    role,
			Content: msg.Content,
		})
	}

	reqBody := ollamaChatRequest{
		Model:    modelName,
		Messages: messages,
		Stream:   false,
	}

	jsonBody, err := json.Marshal(reqBody)

	if err != nil {
		return nil, fmt.Errorf("marshal request: %w", err)
	}

	resp, err := http.Post(
		ollamaBaseURL+"/api/chat",
		"application/json",
		bytes.NewReader(jsonBody),
	)

	if err != nil {
		return nil, fmt.Errorf("ollama request failed: %w", err)
	}

	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("ollama returned status %d", resp.StatusCode)
	}

	var ollamaResp ollamaChatResponse

	if err := json.NewDecoder(resp.Body).Decode(&ollamaResp); err != nil {
		return nil, fmt.Errorf("decode response: %w", err)
	}

	assistantMsg := models.Message{
		ID:      uuid.New(),
		Content: ollamaResp.Message.Content,
		Role:    enums.Assistant,
	}

	return []models.Message{assistantMsg}, nil
}
