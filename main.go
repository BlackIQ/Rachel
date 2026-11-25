package main

import (
	"embed"
	"log"

	"github.com/gin-gonic/gin"

	"github.com/BlackIQ/Rachel/internal/config"
	"github.com/BlackIQ/Rachel/internal/enums"
	"github.com/BlackIQ/Rachel/internal/inits"
	"github.com/BlackIQ/Rachel/internal/router"
)

//go:embed all:frontend/dist
var diskFS embed.FS

func init() {
	if err := inits.Initialize(); err != nil {
		log.Fatalf("[main.go] Error initializing app: %v\n", err)
	}
}

func main() {
	cfg := config.GetConfig()

	if cfg.Environment == enums.Production {
		gin.SetMode(gin.ReleaseMode)
	} else {
		gin.SetMode(gin.DebugMode)
	}

	engine := router.SetupRouter(&diskFS)

	if err := engine.Run(":8000"); err != nil {
		log.Fatalf("Error running app: %v\n", err)
	}
}
