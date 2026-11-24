package agent

import (
	"github.com/google/uuid"

	"github.com/BlackIQ/Rachel/backend/internal/enums"
	"github.com/BlackIQ/Rachel/backend/internal/models"
)

type MessageInput struct {
	Role     enums.MessageRole
	Content  string
	ToolName *string
}

func Run(history []MessageInput) ([]models.Message, error) {
	var lastUserContent string

	for i := len(history) - 1; i >= 0; i-- {
		if history[i].Role == enums.User {
			lastUserContent = history[i].Content

			break
		}
	}

	assistantMsg := models.Message{
		ID:      uuid.New(),
		Content: "You said: " + lastUserContent,
		Role:    enums.Assistant,
	}

	return []models.Message{assistantMsg}, nil
}
