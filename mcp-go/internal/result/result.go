package result

import (
	"encoding/json"
)

type ToolResult struct {
	Success bool           `json:"success"`
	Error   string         `json:"error,omitempty"`
	Message string         `json:"message,omitempty"`
	Data    map[string]any `json:"data,omitempty"`
}

func (r ToolResult) JSON() string {
	b, _ := json.Marshal(r)

	return string(b)
}

func OK(message string, data map[string]any) ToolResult {
	return ToolResult{Success: true, Message: message, Data: data}
}

func Fail(code, message string) ToolResult {
	return ToolResult{Success: false, Error: code, Message: message}
}
