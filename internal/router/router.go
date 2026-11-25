package router

import (
	"embed"
	"io/fs"
	"net/http"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"

	"github.com/BlackIQ/Rachel/internal/handlers"
)

func SetupRouter(diskFS *embed.FS) *gin.Engine {
	router := gin.Default()

	// ===== Frontend ===== //

	frontendFS, err := fs.Sub(*diskFS, "frontend/dist")
	if err != nil {
		panic(err)
	}

	assetsFS, err := fs.Sub(frontendFS, "assets")
	if err != nil {
		panic(err)
	}

	router.StaticFS("/assets", http.FS(assetsFS))

	router.GET("/", func(c *gin.Context) {
		index, err := fs.ReadFile(frontendFS, "index.html")

		if err != nil {
			c.AbortWithStatus(http.StatusInternalServerError)
			return
		}

		c.Data(http.StatusOK, "text/html; charset=utf-8", index)
	})

	// ===== Backend ===== //

	router.Use(cors.Default())

	apiGroup := router.Group("/api")

	chatGroup := apiGroup.Group("/chats")

	chatGroup.GET("", handlers.AllChats)
	chatGroup.GET("/:id", handlers.OneChat)
	chatGroup.POST("", handlers.CreateChat)
	chatGroup.PATCH("/:id", handlers.UpdateChat)
	chatGroup.DELETE("/:id", handlers.DeleteChat)

	messageGroup := apiGroup.Group("/messages")

	messageGroup.GET("/:chatID", handlers.AllMessages)
	messageGroup.POST("/:chatID", handlers.CreateMessage)

	return router
}
