package main

import (
	"log"

	"github.com/gin-gonic/gin"

	"github.com/BlackIQ/Rachel/backend/internal/config"
	"github.com/BlackIQ/Rachel/backend/internal/enums"
	"github.com/BlackIQ/Rachel/backend/internal/inits"
	"github.com/BlackIQ/Rachel/backend/internal/router"
)

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

	engine := router.SetupRouter()

	if err := engine.Run(":8000"); err != nil {
		log.Fatalf("Error running app: %v\n", err)
	}
}
