package agent

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"time"

	mcpsdk "github.com/modelcontextprotocol/go-sdk/mcp"
	"github.com/ollama/ollama/api"

	"github.com/BlackIQ/Rachel/internal/config"
	"github.com/BlackIQ/Rachel/internal/enums"
	"github.com/BlackIQ/Rachel/internal/mcp"
	"github.com/BlackIQ/Rachel/internal/models"
	"github.com/BlackIQ/Rachel/internal/ollama"
)

func Run(parent context.Context, history []models.Message) ([]models.Message, error) {
	cfg := config.GetConfig()
	client := ollama.GetOllama()
	ollamaConfig := cfg.OllamaConfig

	ctx, cancel := context.WithTimeout(parent, 3*time.Minute)
	defer cancel()

	mcpClient, err := mcp.NewClient(ctx)
	if err != nil {
		return nil, fmt.Errorf("mcp client: %w", err)
	}

	defer mcpClient.Close()

	mcpTools, err := mcpClient.ListTools(ctx)
	if err != nil {
		return nil, fmt.Errorf("list tools: %w", err)
	}

	ollamaTools := buildOllamaTools(mcpTools)

	messages := buildOllamaMessages(history)

	if err := client.Heartbeat(ctx); err != nil {
		return nil, errors.New("Ollama is not available: " + err.Error())
	}

	firstResp, err := chat(ctx, client, ollamaConfig, messages, ollamaTools)

	if err != nil {
		return nil, err
	}

	var newMessages []models.Message

	assistantMsg := firstResp.Message
	messages = append(messages, assistantMsg)

	if assistantMsg.Content != "" || assistantMsg.Thinking != "" {
		msg := models.Message{
			Content:  assistantMsg.Content,
			Role:     enums.Assistant,
			Thinking: stringPtr(assistantMsg.Thinking),
		}
		newMessages = append(newMessages, msg)
	}

	toolCalls := assistantMsg.ToolCalls
	if len(toolCalls) == 0 {
		return newMessages, nil
	}

	for _, tc := range toolCalls {
		toolName := tc.Function.Name
		args := toolCallArgsToMap(tc.Function.Arguments)

		toolContent, callErr := mcpClient.CallTool(ctx, toolName, args)
		if callErr != nil {
			toolContent = fmt.Sprintf(`{"success":false,"error":"tool_execution_failed","message":%q}`, callErr.Error())
		}

		toolMsg := api.Message{
			Role:     "tool",
			Content:  toolContent,
			ToolName: toolName,
		}
		messages = append(messages, toolMsg)

		tn := toolName
		newMessages = append(newMessages, models.Message{
			Content:  toolContent,
			Role:     enums.Tool,
			ToolName: &tn,
		})
	}

	finalResp, err := chat(ctx, client, ollamaConfig, messages, ollamaTools)
	if err != nil {
		return nil, err
	}

	finalContent := finalResp.Message.Content
	finalThinking := finalResp.Message.Thinking

	newMessages = append(newMessages, models.Message{
		Content:  finalContent,
		Role:     enums.Assistant,
		Thinking: stringPtr(finalThinking),
	})

	return newMessages, nil
}

func chat(
	ctx context.Context,
	client *api.Client,
	cfg config.OllamaConfig,
	messages []api.Message,
	tools []api.Tool,
) (*api.ChatResponse, error) {
	var resp api.ChatResponse

	req := &api.ChatRequest{
		Model:    cfg.Model,
		Stream:   &cfg.Stream,
		Think:    &cfg.Think,
		Messages: messages,
		Tools:    tools,
	}

	err := client.Chat(ctx, req, func(r api.ChatResponse) error {
		resp = r
		return nil
	})

	if err != nil {
		return nil, errors.New("Error in Ollama Chat: " + err.Error())
	}

	return &resp, nil
}

func buildOllamaMessages(history []models.Message) []api.Message {
	messages := make([]api.Message, 0, len(history))

	for _, m := range history {
		if m.Role == enums.Assistant && m.Content == "" && (m.Thinking == nil || *m.Thinking == "") {
			continue
		}

		msg := api.Message{
			Role:    string(m.Role),
			Content: m.Content,
		}

		if m.Role == enums.Tool && m.ToolName != nil {
			msg.ToolName = *m.ToolName
		}

		messages = append(messages, msg)
	}

	return messages
}

func buildOllamaTools(mcpTools []*mcpsdk.Tool) []api.Tool {
	tools := make([]api.Tool, 0, len(mcpTools))

	for _, t := range mcpTools {
		if t == nil {
			continue
		}

		params := api.ToolFunctionParameters{
			Type: "object",
		}

		if t.InputSchema != nil {
			raw, err := json.Marshal(t.InputSchema)
			if err == nil {
				_ = json.Unmarshal(raw, &params)
			}
		}

		tools = append(tools, api.Tool{
			Type: "function",
			Function: api.ToolFunction{
				Name:        t.Name,
				Description: t.Description,
				Parameters:  params,
			},
		})
	}

	return tools
}

func toolCallArgsToMap(args api.ToolCallFunctionArguments) map[string]any {
	result := make(map[string]any)

	raw, err := json.Marshal(args)

	if err != nil {
		return result
	}

	_ = json.Unmarshal(raw, &result)

	return result
}

func stringPtr(s string) *string {
	if s == "" {
		return nil
	}

	return &s
}
