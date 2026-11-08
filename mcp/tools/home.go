package tools

import (
	"context"
	"encoding/json"
	"net/http"
	"time"

	"github.com/BlackIQ/Rachel/config"
	"github.com/BlackIQ/Rachel/internal/result"
	"github.com/modelcontextprotocol/go-sdk/mcp"
)

func RegisterHome(server *mcp.Server, cfg *config.Config) {
	mcp.AddTool(server, &mcp.Tool{
		Name:        "get_home_temperature",
		Description: "Get the current home temperature information",
	}, func(ctx context.Context, req *mcp.CallToolRequest, _ struct{}) (*mcp.CallToolResult, any, error) {
		return callPico(cfg, "GET", "/api/temperature", func(data map[string]any) result.ToolResult {
			return result.OK("Home sensor reading", map[string]any{
				"temperature": data["temperature"],
				"humidity":    data["humidity"],
			})
		})
	})
}

// تابع کمکی مشترک برای تمام درخواست‌های Pico
func callPico(cfg *config.Config, method, path string, onOK func(map[string]any) result.ToolResult) (*mcp.CallToolResult, any, error) {
	client := &http.Client{Timeout: 5 * time.Second}
	req, err := http.NewRequest(method, cfg.PicoIP+path, nil)
	if err != nil {
		return textResult(result.Fail("pico_error", err.Error())), nil, nil
	}
	req.Header.Set("Authorization", "Bearer "+cfg.PicoSecret)

	resp, err := client.Do(req)
	if err != nil {
		return textResult(result.Fail("pico_unreachable", "Could not reach the Pico device. Check power and network.")), nil, nil
	}
	defer resp.Body.Close()

	var data map[string]any
	if err := json.NewDecoder(resp.Body).Decode(&data); err != nil {
		return textResult(result.Fail("invalid_response", "Pico returned invalid JSON")), nil, nil
	}

	if resp.StatusCode == http.StatusUnauthorized {
		return textResult(result.Fail("auth_failed", "Authentication failed. Check PICO_SECRET and Pico TOKEN.")), nil, nil
	}
	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		msg := "Pico error"
		if m, ok := data["message"].(string); ok {
			msg = m
		}
		return textResult(result.Fail("pico_error", msg)), nil, nil
	}

	return textResult(onOK(data)), nil, nil
}
