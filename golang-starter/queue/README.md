### Getting started

Post a job:

`curl -X POST -H "Content-Type: application/json" -d '{"name": "job one"}' http://localhost:8000/task`

Successful Response:

`{"msg":"task created!"}`

### Basic queue implementation in Golang

1. Creating a job:

```
j := queue.Job{}
j.Name = name
j.Task = queue.CreateTask(func() {
    time.Sleep(10 * time.Millisecond)
    fmt.Print("Task ...1")
})
```

_A job is just a wrapper that contains the name of the job and a task_

2.  put the job in queue

```
if !enqueue(j, jobsChan) {
    return c.JSON(http.StatusOK, struct {
        Msg string `json:"msg"`
    }{
        Msg: "Queue full",
    })
}
```

Complete sample:

_task.go_

```
func CreateJob(name string) queue.Job {
	// Create job
	j := queue.Job{}
	j.Name = name
	j.Task = queue.CreateTask(func() {
		time.Sleep(10 * time.Millisecond)
		fmt.Print("Task ...1")
	})
	return j
}
```

_main.go_

```
j := CreateJob(t.Name)
if !enqueue(j, jobsChan) {
    return c.JSON(http.StatusOK, struct {
        Msg string `json:"msg"`
    }{
        Msg: "Queue full",
    })
}
```

Running:

_Note_ : app uses echo web framework

1. Run the app: `go run main.go task.go`

2. Post request to the server with json data:

```
{
    "name": "task name"
}
```

3. It will return status `200` and `task created` message if successful, otherwise error

4. Task example will be executed after 5 seconds. See file `task.go`
