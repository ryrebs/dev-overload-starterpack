A. Typed

`const a int = 1`

B. Inferred

`const a = 1`

C. Enumerated

- has initial value of zero
- Arithmetic, bitwise operations, bitshifting are allowed at compile time

```
// Block scoped
const (
    zero = iota
	a = iota
	b
    c
)
    fmt.Printf("%v, %T\n", zero, zero) // 0, int
	fmt.Printf("%v, %T\n", a, a) // 1, int
	fmt.Printf("%v, %T", b, b) // 2, int
    fmt.Printf("%v, %T", c, c) // 3, int

// Resets value
const a = iota
const b = iota

    fmt.Printf("%v, %T\n", a, a) // 0, int
	fmt.Printf("%v, %T", b, b) // 0, int
```
