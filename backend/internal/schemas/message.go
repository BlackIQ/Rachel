package schemas

type CreateMessageRequest struct {
	Content string `json:"content" binding:"required"`
}
