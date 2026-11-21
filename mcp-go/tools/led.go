package tools

import (
	"context"
	"fmt"

	"github.com/BlackIQ/Rachel/config"
	"github.com/BlackIQ/Rachel/internal/result"
	"github.com/modelcontextprotocol/go-sdk/mcp"
)

var validLEDs = map[string]bool{
	"white": true, "green": true, "red": true, "blue": true,
}

type LEDArgs struct {
	Name string `json:"name" jsonschema:"LED name. One of: white, green, red, blue"`
}

func RegisterLED(server *mcp.Server, cfg *config.Config) {
	mcp.AddTool(server, &mcp.Tool{
		Name:        "turn_led_on",
		Description: "Turn on a specific LED on the Rachel Pico device",
	}, ledHandler(cfg, "on"))

	mcp.AddTool(server, &mcp.Tool{
		Name:        "turn_led_off",
		Description: "Turn off a specific LED on the Rachel Pico device",
	}, ledHandler(cfg, "off"))
}

func ledHandler(cfg *config.Config, action string) func(context.Context, *mcp.CallToolRequest, LEDArgs) (*mcp.CallToolResult, any, error) {
	return func(ctx context.Context, req *mcp.CallToolRequest, args LEDArgs) (*mcp.CallToolResult, any, error) {
		if !validLEDs[args.Name] {
			return textResult(result.Fail("unknown_led", fmt.Sprintf("Unknown LED: %s", args.Name))), nil, nil
		}
		path := fmt.Sprintf("/api/leds/%s/%s", args.Name, action)
		return callPico(cfg, "POST", path, func(data map[string]any) result.ToolResult {
			msg := fmt.Sprintf("LED %s is now %s", args.Name, action)
			if m, ok := data["message"].(string); ok {
				msg = m
			}
			return result.OK(msg, nil)
		})
	}
}
