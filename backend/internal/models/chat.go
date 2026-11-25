package models

import (
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type Chat struct {
	ID        uuid.UUID      `gorm:"column:id; type:uuid; primaryKey" json:"id"`
	Title     string         `gorm:"column:title; not null" json:"title"`
	Messages  []*Message     `gorm:"foreignKey:ChatID; references:ID" json:"messages"`
	CreatedAt time.Time      `gorm:"column:created_at" json:"createdAt"`
	UpdatedAt time.Time      `gorm:"column:updated_at" json:"updatedAt"`
	DeletedAt gorm.DeletedAt `gorm:"column:deleted_at; index" json:"-"`
}
