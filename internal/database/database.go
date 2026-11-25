package database

import (
	"errors"

	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

var db *gorm.DB

func InitDB() (err error) {
	dialector := sqlite.Open("rachel.db")

	connection, err := gorm.Open(dialector, &gorm.Config{})

	if err != nil {
		return errors.New("[database.go] DB Connection: " + err.Error())
	}

	if err := Migration(connection); err != nil {
		return errors.New("[database.py] DB Migration:" + err.Error())
	}

	db = connection

	return nil
}

func GetDB() *gorm.DB {
	return db
}
