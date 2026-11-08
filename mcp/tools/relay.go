package tools

import (
	"context"
	"fmt"

	"github.com/BlackIQ/Rachel/config"
	"github.com/BlackIQ/Rachel/internal/result"
	"github.com/modelcontextprotocol/go-sdk/mcp"
)

var validRelays = map[string]bool{
	"library": true, "bedroom": true, "living_room": true,
	"kitchen": true, "r1": true, "r2": true, "r3": true, "r4": true,
}

type RelayArgs struct {
	Name string `json:"name" jsonschema:"Relay name. One of: library, bedroom, living_room, kitchen, r1, r2, r3, r4"`
}

func RegisterRelay(server *mcp.Server, cfg *config.Config) {
	mcp.AddTool(server, &mcp.Tool{
		Name:        "turn_relay_on",
		Description: "Turn on a specific relay on the Rachel Pico device",
	}, relayHandler(cfg, "on"))

	mcp.AddTool(server, &mcp.Tool{
		Name:        "turn_relay_off",
		Description: "Turn off a specific relay on the Rachel Pico device",
	}, relayHandler(cfg, "off"))
}

func relayHandler(cfg *config.Config, action string) func(context.Context, *mcp.CallToolRequest, RelayArgs) (*mcp.CallToolResult, any, error) {
	return func(ctx context.Context, req *mcp.CallToolRequest, args RelayArgs) (*mcp.CallToolResult, any, error) {
		if !validRelays[args.Name] {
			return textResult(result.Fail("unknown_relay", fmt.Sprintf("Unknown relay: %s", args.Name))), nil, nil
		}
		path := fmt.Sprintf("/api/relays/%s/%s", args.Name, action)
		return callPico(cfg, "POST", path, func(data map[string]any) result.ToolResult {
			msg := fmt.Sprintf("Relay %s is now %s", args.Name, action)
			if m, ok := data["message"].(string); ok {
				msg = m
			}
			return result.OK(msg, nil)
		})
	}
}
