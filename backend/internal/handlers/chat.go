package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func AllChats(ctx *gin.Context) {
	ctx.Status(http.StatusOK)
}

func OneChat(ctx *gin.Context) {
	ctx.Status(http.StatusOK)
}

func CreateChat(ctx *gin.Context) {
	ctx.Status(http.StatusOK)
}

func UpdateChat(ctx *gin.Context) {
	ctx.Status(http.StatusOK)
}

func DeleteChat(ctx *gin.Context) {
	ctx.Status(http.StatusOK)
}
