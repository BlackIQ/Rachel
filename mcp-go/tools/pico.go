package tools

import (
	"context"

	"github.com/BlackIQ/Rachel/config"
	"github.com/BlackIQ/Rachel/internal/result"
	"github.com/modelcontextprotocol/go-sdk/mcp"
)

func RegisterPico(server *mcp.Server, cfg *config.Config) {
	mcp.AddTool(server, &mcp.Tool{
		Name:        "get_pico_resources",
		Description: "Get Raspberry Pi Pico memory information",
	}, func(ctx context.Context, req *mcp.CallToolRequest, _ struct{}) (*mcp.CallToolResult, any, error) {
		return callPico(cfg, "GET", "/api/system/memory", func(data map[string]any) result.ToolResult {
			return result.OK("Pico memory reading", map[string]any{
				"free":      data["free"],
				"allocated": data["allocated"],
			})
		})
	})
}
