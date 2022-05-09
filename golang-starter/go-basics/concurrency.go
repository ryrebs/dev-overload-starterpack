package main

import (
	"fmt"
	"time"
)

func main() {
	fmt.Println("Start generator")
	startGenerator()
	fmt.Println("Start without multiplexing")
	withoutMultiplexing()
	fmt.Println("Start with multiplexing")
	withMultiplexing()
}

func startGenerator() {
	ch := boring("boring")
	for i := 0; i < 5; i++ {
		fmt.Printf("You say %q\n", <-ch)
	}
	fmt.Println("-----------------")
}

// A. Generator function, returns a receive-only channel
func boring(msg string) <-chan string {
	c := make(chan string)
	go func() {
		for i := 0; ; i++ {
			c <- fmt.Sprintf("%s %d", msg, i)
			time.Sleep(time.Second)
		}
	}()
	return c
}

func withoutMultiplexing() {
	ch1 := boring("boring ch1")
	ch2 := boring("boring ch2")

	for i := 0; i < 5; i++ {
		// Without multiplexing these will execute on an alternate manner
		// because of blocking condition
		fmt.Printf("You say %q\n", <-ch1)
		fmt.Printf("You say %q\n", <-ch2)
	}
	fmt.Println("-----------------")
}

func withMultiplexing() {
	ch := multiplexer(boring("boring ch1"), boring("boring ch2"))

	for i := 0; i < 10; i++ {
		// Receives value from 2 channels without each blocking each other
		fmt.Printf("You say %q\n", <-ch)
	}
	fmt.Println("-----------------")
}

// B. Multiplexing
func multiplexer(ch1, ch2 <-chan string) <-chan string {
	ch := make(chan string)
	// Execute independently using goroutine to avoid blocking
	go func() {
		for {
			ch <- <-ch1
		}
	}()
	go func() {
		for {
			ch <- <-ch2
		}
	}()
	return ch
}

// Multiplexing can be done also with *select
