package main

import (
	"log"

	"github.com/BlackIQ/Rachel/backend/internal/router"
)

func main() {
	engine := router.SetupRouter()

	if err := engine.Run(":8080"); err != nil {
		log.Fatalf("Error running app: %v\n", err)
	}
}
