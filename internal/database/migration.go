package database

import (
	"errors"

	"gorm.io/gorm"

	"github.com/BlackIQ/Rachel/backend/internal/models"
)

func Migration(db *gorm.DB) (err error) {
	// Chat
	if err := db.AutoMigrate(&models.Chat{}); err != nil {
		return errors.New("[migration.py] Can't migrate Chat:" + err.Error())
	}

	// Message
	if err := db.AutoMigrate(&models.Message{}); err != nil {
		return errors.New("[migration.py] Can't migrate Message:" + err.Error())
	}

	return nil
}
