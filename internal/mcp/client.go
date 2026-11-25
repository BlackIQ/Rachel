package mcp

import (
	"context"
	"encoding/json"
	"fmt"
	"strings"

	"github.com/modelcontextprotocol/go-sdk/mcp"
)

const defaultMCPEndpoint = "http://127.0.0.1:8008/mcp"

type Client struct {
	session *mcp.ClientSession
}

func NewClient(ctx context.Context) (*Client, error) {
	client := mcp.NewClient(&mcp.Implementation{
		Name:    "rachel-backend",
		Version: "1.0.0",
	}, nil)

	session, err := client.Connect(ctx, &mcp.StreamableClientTransport{
		Endpoint: defaultMCPEndpoint,
	}, nil)
	if err != nil {
		return nil, fmt.Errorf("mcp connect failed: %w", err)
	}

	return &Client{session: session}, nil
}

func (c *Client) Close() error {
	if c.session != nil {
		return c.session.Close()
	}
	return nil
}

func (c *Client) ListTools(ctx context.Context) ([]*mcp.Tool, error) {
	result, err := c.session.ListTools(ctx, nil)

	if err != nil {
		return nil, fmt.Errorf("list tools failed: %w", err)
	}

	return result.Tools, nil
}

func (c *Client) CallTool(ctx context.Context, name string, arguments map[string]any) (string, error) {
	result, err := c.session.CallTool(ctx, &mcp.CallToolParams{
		Name:      name,
		Arguments: arguments,
	})

	if err != nil {
		return "", fmt.Errorf("call tool %q failed: %w", name, err)
	}

	return serializeToolResult(result), nil
}

func serializeToolResult(result *mcp.CallToolResult) string {
	if result == nil {
		return `{"success":false,"error":"empty result"}`
	}

	if result.StructuredContent != nil {
		b, err := json.Marshal(result.StructuredContent)
		if err == nil {
			return string(b)
		}
	}

	var parts []string
	for _, content := range result.Content {
		if tc, ok := content.(*mcp.TextContent); ok && tc.Text != "" {
			parts = append(parts, tc.Text)
		}
	}

	if len(parts) > 0 {
		return strings.Join(parts, "\n")
	}

	if result.IsError {
		return `{"success":false,"error":"tool returned error"}`
	}

	return `{"success":true}`
}
