package inits

import (
	"errors"

	"github.com/BlackIQ/Rachel/backend/internal/database"
)

func InitDB() (err error) {
	if err := database.InitDB(); err != nil {
		return errors.New("[database.go] Can't init database: " + err.Error())
	}

	return nil
}
