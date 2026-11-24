package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func AllMessages(ctx *gin.Context) {
	ctx.Status(http.StatusOK)
}

func CreateMessage(ctx *gin.Context) {
	ctx.Status(http.StatusOK)
}
