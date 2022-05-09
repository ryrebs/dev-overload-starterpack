package queue

// Task type
type Task struct {
	T func()
}

// Execute task
func (T *Task) Execute() {
	T.T()
}

// CreateTask task
func CreateTask(f func()) Task {
	return Task{f}
}
