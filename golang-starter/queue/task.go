package main

import (
	"fmt"
	"gettingstarted/queue/queue"
	"time"
)

// CreateJob  define your tasks here
func CreateJob(name string) queue.Job {
	// Create job
	j := queue.Job{}
	j.Name = name
	j.Task = queue.CreateTask(func() {
		fmt.Print("I'm doing something!")
		time.Sleep(5000 * time.Millisecond)
	})
	return j
}
