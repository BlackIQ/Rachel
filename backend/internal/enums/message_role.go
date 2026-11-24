package enums

type MessageRole string

const (
	USER      MessageRole = "user"
	ASSISTANT MessageRole = "assistant"
	TOOL      MessageRole = "tool"
	SYSTEM    MessageRole = "system"
)
