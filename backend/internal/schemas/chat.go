package schemas

type CreateChatRequest struct {
	Title string `json:"title" binding:"required"`
}

type UpdateChatRequest struct {
	Title *string `json:"title"`
}
