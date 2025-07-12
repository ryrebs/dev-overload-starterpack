A. Simple use, case should not overlap

```go
switch choice := 1; choice {
case 1:
    fmt.Println("1")
case 2, 4, 6:
    fmt.Println("2, 4, 6")
default:
    fmt.Println("Invalid choice")
} // 1
```

B. Tagless, case can overlap, runs the first matching case

```go
choice := 1
switch {
case choice == 1:
    fmt.Println("1")
case choice > 0:
    fmt.Println("1, 2, 3")
default:
    fmt.Println("Invalid choice")
} // 1
```

C. Fallthrough - executes next case

```go
choice2 := 1
switch {
case choice2 == 1:
    fmt.Println("1")
    fallthrough
case choice2 > 0:
    fmt.Println("1, 2, 3")
default:
    fmt.Println("Invalid choice")
}
// 1
// 1, 2, 3
```
