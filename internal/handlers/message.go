package handlers

import (
	"errors"
	"log"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"gorm.io/gorm"

	"github.com/BlackIQ/Rachel/backend/internal/database"
	"github.com/BlackIQ/Rachel/backend/internal/enums"
	"github.com/BlackIQ/Rachel/backend/internal/models"
	"github.com/BlackIQ/Rachel/backend/internal/schemas"
	"github.com/BlackIQ/Rachel/backend/internal/services/agent"
)

func AllMessages(ctx *gin.Context) {
	chatID, err := uuid.Parse(ctx.Param("chatID"))

	if err != nil {
		ctx.AbortWithStatusJSON(
			http.StatusBadRequest,
			gin.H{"message": "Invalid Chat ID"},
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

	var messages []models.Message

	result = db.Where("chat_id = ?", chatID).Order("created_at ASC").Find(&messages)

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
	chatID, err := uuid.Parse(ctx.Param("chatID"))

	if err != nil {
		ctx.AbortWithStatusJSON(
			http.StatusBadRequest,
			gin.H{"message": "Invalid Chat ID"},
		)
		return
	}

	var messageData schemas.CreateMessageRequest

	if err := ctx.ShouldBindBodyWithJSON(&messageData); err != nil {
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

	userMessage := models.Message{
		ID:      uuid.New(),
		Content: messageData.Content,
		Role:    enums.User,
		ChatID:  chat.ID,
	}

	if err := db.Create(&userMessage).Error; err != nil {
		ctx.AbortWithStatusJSON(
			http.StatusInternalServerError,
			gin.H{"message": "Database error"},
		)
		return
	}

	var dbMessages []models.Message

	result = db.Where("chat_id = ?", chat.ID).Order("created_at ASC").Find(&dbMessages)

	if result.Error != nil {
		ctx.AbortWithStatusJSON(
			http.StatusInternalServerError,
			gin.H{"message": "Database error"},
		)
		return
	}

	newMessages, err := agent.Run(ctx.Request.Context(), dbMessages)

	if err != nil {
		ctx.AbortWithStatusJSON(
			http.StatusInternalServerError,
			gin.H{"message": "Ollama error"},
		)
		return
	}

	var lastAssistant *models.Message

	for i := range newMessages {
		newMessages[i].ID = uuid.New()
		newMessages[i].ChatID = chat.ID

		if err := db.Create(&newMessages[i]).Error; err != nil {
			ctx.AbortWithStatusJSON(
				http.StatusInternalServerError,
				gin.H{"message": "Database error"},
			)

			return
		}

		if newMessages[i].Role == enums.Assistant {
			lastAssistant = &newMessages[i]
		}
	}

	db.Model(&chat).Update("updated_at", time.Now())

	if result.Error != nil {
		log.Printf("Error saving time %v\n", result.Error.Error())
	}

	if lastAssistant != nil {
		ctx.JSON(http.StatusCreated, lastAssistant)
		return
	}

	ctx.JSON(
		http.StatusCreated,
		userMessage,
	)
}
