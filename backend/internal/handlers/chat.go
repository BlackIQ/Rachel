package handlers

import (
	"errors"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"gorm.io/gorm"

	"github.com/BlackIQ/Rachel/backend/internal/database"
	"github.com/BlackIQ/Rachel/backend/internal/models"
	"github.com/BlackIQ/Rachel/backend/internal/schemas"
)

func AllChats(ctx *gin.Context) {
	db := database.GetDB()

	var chats []models.Chat

	result := db.Order("updated_at ASC").Find(&chats)

	if result.Error != nil {
		ctx.AbortWithStatusJSON(
			http.StatusInternalServerError,
			gin.H{"message": "Database error"},
		)
		return
	}

	ctx.JSON(
		http.StatusOK,
		chats,
	)
}

func OneChat(ctx *gin.Context) {
	chatID, err := uuid.Parse(ctx.Param("id"))

	if err != nil {
		ctx.AbortWithStatusJSON(
			http.StatusBadRequest,
			gin.H{"message": "Invalid ID"},
		)
		return
	}

	db := database.GetDB()

	var chat models.Chat

	result := db.Where("id = ?", chatID).First(&chat)

	if errors.Is(result.Error, gorm.ErrRecordNotFound) {
		ctx.AbortWithStatusJSON(
			http.StatusNotFound,
			gin.H{"message": "Chat not found"},
		)
		return
	}

	if result.Error != nil {
		ctx.AbortWithStatusJSON(
			http.StatusInternalServerError,
			gin.H{"message": "Database error"},
		)
		return
	}

	ctx.JSON(
		http.StatusOK,
		chat,
	)
}

func CreateChat(ctx *gin.Context) {
	var chatData schemas.CreateChatRequest

	if err := ctx.ShouldBindBodyWithJSON(&chatData); err != nil {
		ctx.AbortWithStatusJSON(
			http.StatusBadRequest,
			gin.H{"message": err.Error()},
		)
		return
	}

	db := database.GetDB()

	newChat := models.Chat{
		ID:    uuid.New(),
		Title: chatData.Title,
	}

	result := db.Create(&newChat)

	if result.Error != nil {
		ctx.AbortWithStatusJSON(
			http.StatusInternalServerError,
			gin.H{"message": "Database error"},
		)
		return
	}

	ctx.JSON(
		http.StatusCreated,
		newChat,
	)
}

func UpdateChat(ctx *gin.Context) {
	chatID, err := uuid.Parse(ctx.Param("id"))

	if err != nil {
		ctx.AbortWithStatusJSON(
			http.StatusBadRequest,
			gin.H{"message": "Invalid ID"},
		)
		return
	}

	var chatData schemas.UpdateChatRequest

	if err := ctx.ShouldBindBodyWithJSON(&chatData); err != nil {
		ctx.AbortWithStatusJSON(
			http.StatusBadRequest,
			gin.H{"message": err.Error()},
		)
		return
	}

	db := database.GetDB()

	var chat models.Chat

	result := db.Where("id = ?", chatID).First(&chat)

	if errors.Is(result.Error, gorm.ErrRecordNotFound) {
		ctx.AbortWithStatusJSON(
			http.StatusNotFound,
			gin.H{"message": "Chat not found"},
		)
		return
	}

	if result.Error != nil {
		ctx.AbortWithStatusJSON(
			http.StatusInternalServerError,
			gin.H{"message": "Database error"},
		)
		return
	}

	updates := map[string]any{}

	if chatData.Title != nil {
		updates["Title"] = chatData.Title
	}

	result = db.Model(&chat).Updates(updates)

	if result.Error != nil {
		ctx.AbortWithStatusJSON(
			http.StatusInternalServerError,
			gin.H{"message": "Database error"},
		)
		return
	}

	ctx.JSON(
		http.StatusOK,
		chat,
	)

}

func DeleteChat(ctx *gin.Context) {
	chatID, err := uuid.Parse(ctx.Param("id"))

	if err != nil {
		ctx.AbortWithStatusJSON(
			http.StatusBadRequest,
			gin.H{"message": "Invalid ID"},
		)
		return
	}

	db := database.GetDB()

	var chat models.Chat

	result := db.Where("id = ?", chatID).First(&chat)

	if errors.Is(result.Error, gorm.ErrRecordNotFound) {
		ctx.AbortWithStatusJSON(
			http.StatusNotFound,
			gin.H{"message": "Chat not found"},
		)
		return
	}

	if result.Error != nil {
		ctx.AbortWithStatusJSON(
			http.StatusInternalServerError,
			gin.H{"message": "Database error"},
		)
		return
	}

	result = db.Delete(&chat)

	if result.RowsAffected == 0 {
		ctx.AbortWithStatusJSON(
			http.StatusNotFound,
			gin.H{"message": "Chat not found"},
		)
		return
	}

	ctx.Status(
		http.StatusNoContent,
	)
}
