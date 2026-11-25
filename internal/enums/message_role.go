package enums

type MessageRole string

const (
	User      MessageRole = "user"
	Assistant MessageRole = "assistant"
	Tool      MessageRole = "tool"
	System    MessageRole = "system"
)
