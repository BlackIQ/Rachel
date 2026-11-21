package tools

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"github.com/BlackIQ/Rachel/config"
	"github.com/BlackIQ/Rachel/internal/result"
	"github.com/modelcontextprotocol/go-sdk/mcp"
)

type WeatherArgs struct {
	City string `json:"city" jsonschema:"the name of the city"`
}

func RegisterWeather(server *mcp.Server, cfg *config.Config) {
	mcp.AddTool(server, &mcp.Tool{
		Name:        "get_weather",
		Description: "Get the current weather information for a city",
	}, func(ctx context.Context, req *mcp.CallToolRequest, args WeatherArgs) (*mcp.CallToolResult, any, error) {
		if cfg.WeatherAPIKey == "" {
			return textResult(result.Fail("missing_api_key", "Weather API key is not set in .env")), nil, nil
		}

		client := &http.Client{Timeout: 8 * time.Second}
		url := fmt.Sprintf("https://api.weatherapi.com/v1/current.json?q=%s&key=%s", args.City, cfg.WeatherAPIKey)

		resp, err := client.Get(url)
		if err != nil {
			return textResult(result.Fail("network_error", "Could not reach WeatherAPI. Check your internet connection.")), nil, nil
		}
		defer resp.Body.Close()

		var data map[string]any
		if err := json.NewDecoder(resp.Body).Decode(&data); err != nil {
			return textResult(result.Fail("invalid_response", "WeatherAPI returned invalid JSON")), nil, nil
		}

		if resp.StatusCode != http.StatusOK {
			msg := "Unknown weather API error"
			if errObj, ok := data["error"].(map[string]any); ok {
				if m, ok := errObj["message"].(string); ok {
					msg = m
				}
			}
			return textResult(result.Fail("weather_api_error", msg)), nil, nil
		}

		return textResult(result.OK(fmt.Sprintf("Weather for %s", args.City), data)), nil, nil
	})
}

func textResult(r result.ToolResult) *mcp.CallToolResult {
	return &mcp.CallToolResult{
		Content: []mcp.Content{
			&mcp.TextContent{Text: r.JSON()},
		},
	}
}
