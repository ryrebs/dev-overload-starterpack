A. Channels is the way for the goroutine to communicate with each other by sending and receiving data of specified element type.
([Source](https://golang.org/ref/spec#Channel_types))

```
var wg = sync.WaitGroup{}

func main() {
	// 1. Create the channel
	ch := make(chan int)

	// 2. Add 2 goroutine to the waiting group
	wg.Add(2)

	// 3. Create the goroutine that receives from the channel
	go func() {
		i := <-ch // receive
		fmt.Println(i)
		wg.Done()
	}()

	// Create the goroutine that sends to the channel
	go func() {
		// sending to (passes a copy), blocking statement until a receiver is found
		ch <- 1
		wg.Done()
	}()

	// For all all goroutines to finish
	wg.Wait()

}

```

B. Organizing goroutines to do specific job only, which is either receive or send

```
// receiving only
go func(ch <-chan int) {
    i := <-ch
    fmt.Println(i)
    wg.Done()
}(ch)

// sending only
go func(ch chan<- int) {
    ch <- 1
    wg.Done()
}(ch)
```

C. Buffered channels creates storage to accept multiple incoming data

```
// creates 50 int storage
ch := make(chan int, 50)
```

D. Looping through channel

```
go func(ch <-chan int) {
    for i := range ch {
        fmt.Println(i)
    }
    wg.Done()
}(ch)


go func(ch chan<- int) {
    ch <- 1
    ch <- 2
	// Signals that channel has stopped receiving data.
    close(ch)
    wg.Done()
}(ch)
```

E. Waiting on multiple communication operations through `select`

```

func main() {
	ch := make(chan int)
	exitCh := make(chan struct{})
	limit := 10

	go func(limit int) {
		fmt.Println("Start square")
		// reads 10 data on ch channel
		for i := 0; i < limit; i++ {
			fmt.Println(<-ch)
		}
		// send a data to exitCh to signal an exit
		exitCh <- struct{}{}
	}(limit)
	square(ch, exitCh)
}

func square(ch chan int, exitCh chan struct{}) {
	n := 2
	// Notice the infinite loop
	for {
		select {
		// sends data to ch channel
		case ch <- n:
			n = n * 2
		// reads data to existCh channel
		case <-exitCh:
			fmt.Println("Done square")
			// exit the loop
			return
		}
	}
}

/** Output
Start square
2
4
8
16
32
64
128
256
512
1024
Done square
*/
```
