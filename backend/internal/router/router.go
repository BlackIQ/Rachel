package router

import (
	"net/http"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"

	"github.com/BlackIQ/Rachel/backend/internal/handlers"
)

func SetupRouter() *gin.Engine {
	router := gin.Default()

	router.Use(cors.Default())

	router.GET("/", func(ctx *gin.Context) {
		ctx.JSON(
			http.StatusOK,
			gin.H{
				"message": "Router",
			},
		)
	})

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
