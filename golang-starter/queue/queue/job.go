package queue

// Job type
type Job struct {
	Name string `json:"name" validate:"required"`
	Task Task
}
