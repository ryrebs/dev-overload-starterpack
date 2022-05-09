A. Panick - when application can not continue to function / execute - unrecoverable events

```
// import fmt and panic
fmt.Println("start")
panic("Something bad happened")
fmt.Println("end") // unreachable
// start
// panic: Something bad happened
// some detailed errors here...

```

B. Use `recover` to recover from `panic`. Use only inside `defer` functions

```
package main

import (
	"fmt"
	"log"
)

// import fmt, panic, log
func main() {
	fmt.Println("start")
	// higher function in call stack will continue unless panic is re throwed
	panicker()
	// Executed if panic is handled and not re throwed
	fmt.Println("end")
}

func panicker() {
	fmt.Println("panic start")
	defer func() {
		if err := recover(); err != nil {
			log.Println("Recovering Error: ", err) // gets the panic error

			// with re-panic, this function will panic and not continue
			// panic(err) // this will re throw the panic and stops the caller
			// start
			// panic start
			// Recovering Error: ...
			// Panic details ...
		}
	}()
	panic("something bad happened")
}

// without repanic
// start
// panic start
// Recovering Error: ...
// end
```
