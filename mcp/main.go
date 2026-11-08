package main

import (
	"context"
	"log"
	"os"

	"github.com/BlackIQ/Rachel/config"
	"github.com/BlackIQ/Rachel/tools"
	"github.com/modelcontextprotocol/go-sdk/mcp"
)

func main() {
	cfg := config.Load()

	server := mcp.NewServer(&mcp.Implementation{
		Name:    "Rachel Assistant MCP Server",
		Version: "0.1.0",
	}, nil)

	tools.RegisterWeather(server, cfg)
	tools.RegisterHome(server, cfg)
	tools.RegisterPico(server, cfg)
	tools.RegisterLED(server, cfg)
	tools.RegisterRelay(server, cfg)

	if err := server.Run(context.Background(), &mcp.StdioTransport{}); err != nil {
		log.Printf("Server failed: %v", err)
		os.Exit(1)
	}
}
