A. Passing multiple arguments with the same type

```
greet("Hi", "Ed") // Hi Ed

func greet(msg, name string) { // parameter, parameter type
	fmt.Println(msg, name)
}
```

B. Passing pointer type argument

```
name := "Edy"
msg := "Hello"
greet2(&msg, &name) // Hello Edy

func greet2(msg, name *string) { // parameter, parameter type
	fmt.Println(*msg, *name)
}
```

C. Variatic parameter

```
greet3("Hello", "Ed", "Edy") // Hello [Ed Edy]

func greet3(msg string, names ...string) {
	fmt.Println(msg, names)
}

```

D. Return value

```
fmt.Println(greet4("Hellooo")) // Echoed Hellooo


func greet4(msg string) string {
	return "Echoed " + msg
}
```

E. Return a pointer - pointer return value is created on Heap rather than the stack,
since variables in the function is created on that function's stack
and deleted after the function executes or returns

```
func sum(values ...int) *int {
	result := 0
	// some logic here
	return &result // allocate to heap
}
```

E. Named return value

```
fmt.Println(greet5("Heyy")) // Heyy echoed

func greet5(msg string) (echo string) {
	echo = msg + " " + "echoed"
	return
}
```

F. Returning multiple value from function call

```
func main() {
	d, err := divide(5.0, 0.0)
	// some error checking here
	// err != nil
	fmt.Println(d, err)
}

func divide(a, b float64) (float64, error) {
	if b == 0.0 {
		return 0.0, fmt.Errorf("cannot divide by zero")
	}
	return a / b, nil
}
```

G. Anonymous function and immediately invoke function

```
func main() {
	func() {
		// some logic here
	} ()
}
```

H. Function as variable

```
f := func() {
	fmt.Println("Function variable")
}
f()
```

I. Method

```
func main() {
	g := greeter{
		greeting: "Hello",
		name:     "Go",
	}
	g.greet() //  Hello Go

}

type greeter struct {
	greeting string
	name     string
}

// method greet
func (g greeter) greet() { // (g greeter) is a value receiver - operating on a copy
	fmt.Println(g.greeting, g.name)
}
// func (g *greeter) greet() {}  - // (g greeter) is a pointer receiver - operating on a pointer
```
