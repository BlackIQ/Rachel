package models

import (
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"

	"github.com/BlackIQ/Rachel/backend/internal/enums"
)

type Message struct {
	ID        uuid.UUID         `gorm:"column:id; type:uuid; primaryKey" json:"id"`
	Content   string            `gorm:"column:content; type:text; not null" json:"content"`
	Thinking  *string           `gorm:"column:thinking; type:text" json:"thinking"`
	Role      enums.MessageRole `gorm:"column:role; type:varchar(20); not null" json:"role"`
	ToolName  *string           `gorm:"column:tool_name; type:varchar(100)" json:"toolName"`
	ChatID    uuid.UUID         `gorm:"column:chat_id; type:uuid; not null;index" json:"-"`
	Chat      *Chat             `gorm:"foreignKey:ChatID; references:ID" json:"-"`
	CreatedAt time.Time         `gorm:"column:created_at" json:"createdAt"`
	UpdatedAt time.Time         `gorm:"column:updated_at" json:"updatedAt"`
	DeletedAt gorm.DeletedAt    `gorm:"column:deleted_at;index" json:"-"`
}
