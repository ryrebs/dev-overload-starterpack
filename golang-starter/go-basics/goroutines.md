A. Goroutines - independently executing functions. Lightweight threads compared to OS threads

```
import (
	"fmt"
	"time"
)

func main() {

	msg := "Hey!"
	go func(msg string) {
		// variables can be still accessible without passing it as argument
		// because of closure property
		fmt.Println(msg)
	}(msg)
	time.Sleep(100 * time.Millisecond)
	// Hey!
}
```

B. Using wait group instead of sleep

```
import (
	"fmt"
	"sync"
)

var wg = sync.WaitGroup{}

func main() {
	msg := "Hey!"

    // add 1 goroutine
	wg.Add(1)
	go func(msg string) {
		// variables can be still accessible without passing it as argument
		// because of closure property
		fmt.Println(msg)
		wg.Done()
	}(msg)

    // wait for all goroutines to finish
	wg.Wait()
	// Hey!
}
```

C. Multiple goroutines that executes without synchronization or without order

```
var wg = sync.WaitGroup{}
var counter = 0

func main() {
	for i := 0; i < 10; i++ {
		wg.Add(2)
		// Randomly executes out of order
		go increment()
		go sayHey()
	}
	wg.Wait()
}

func sayHey() {
	fmt.Printf("Hey, count: %v\n", counter)
	wg.Done()
}

func increment() {
	counter++
	wg.Done()
}
```

D. Using _mutex_ to lock and unlock a part of code.

- _Locks and unlocks during writing and reading a variable_ to avoid race conditions
- _GOMAXPROCS variable limits the number of operating system threads that can execute user-level Go code simultaneously_
  .([source](https://golang.org/pkg/runtime/#GOMAXPROCS))

```
var wg = sync.WaitGroup{}
var m = sync.RWMutex{}

var counter = 0

func main() {
	runtime.GOMAXPROCS(100)
	for i := 0; i < 10; i++ {
		wg.Add(2)
		// we want to read lock sayHey to protect from goroutine executing a read successively
		m.RLock()
		go sayHey()
		// we want to write lock sayHey to protect from goroutine executing a write successively
		m.Lock()
		go increment()
	}
	wg.Wait()
}

func sayHey() {
	fmt.Printf("Hey, count: %v\n", counter)
	m.RUnlock()
	wg.Done()
}

func increment() {
	counter++
	m.Unlock()
	wg.Done()
}

/** Ouputs:
Hey, count: 0
Hey, count: 1
Hey, count: 2
Hey, count: 3
Hey, count: 4
Hey, count: 5
Hey, count: 6
Hey, count: 7
Hey, count: 8
Hey, count: 9
*/
```
