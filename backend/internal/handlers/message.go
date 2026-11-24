package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"

	"github.com/BlackIQ/Rachel/backend/internal/database"
	"github.com/BlackIQ/Rachel/backend/internal/models"
)

func AllMessages(ctx *gin.Context) {
	chatID, err := uuid.Parse(ctx.Param("chatID"))

	if err != nil {
		ctx.AbortWithStatusJSON(
			http.StatusBadRequest,
			gin.H{"message": "Invalid ID"},
		)
		return
	}

	var messages []models.Message

	db := database.GetDB()

	result := db.Where("chat_id = ?", chatID).Order("created_at ASC").Find(&messages)

	if result.Error != nil {
		ctx.AbortWithStatusJSON(
			http.StatusInternalServerError,
			gin.H{"message": "Database error"},
		)
		return
	}

	ctx.JSON(
		http.StatusOK,
		messages,
	)
}

func CreateMessage(ctx *gin.Context) {
	ctx.Status(http.StatusOK)
}
