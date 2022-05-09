package main

import (
	"fmt"
	"net/http"

	"gettingstarted/queue/queue"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

const MAX_JOBS int = 100
const MAX_WORKER int = 10

var jobsChan = make(chan queue.Job, MAX_JOBS)

func enqueue(j queue.Job, jobs chan<- queue.Job) bool {
	select {
	case jobs <- j:
		return true
	default:
		return false
	}
}

func worker(jChan <-chan queue.Job) {
	for j := range jChan {
		fmt.Println("Executing", j.Name)
		j.Task.Execute()
		fmt.Println("\nExecuting " + j.Name + " Done!")
	}
}

func createWorkerPool() {
	for i := 0; i <= MAX_WORKER; i++ {
		go worker(jobsChan)
	}
}

func main() {

	e := echo.New()
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())
	e.Use(middleware.Secure())

	e.POST("/task", func(c echo.Context) (err error) {
		t := new(struct {
			Name string `json:"name" validate:"required,gt=5"`
		})
		if err = c.Bind(t); err != nil {
			return
		}
		// Create your job
		j := CreateJob(t.Name)

		// Put the job in queue
		if !enqueue(j, jobsChan) {
			return c.JSON(http.StatusOK, struct {
				Msg string `json:"msg"`
			}{
				Msg: "Queue full",
			})
		}

		return c.JSON(http.StatusOK, struct {
			Msg string `json:"msg"`
		}{
			Msg: "Task created!",
		})
	})

	createWorkerPool()
	e.Logger.Fatal(e.Start(":8000"))

}
