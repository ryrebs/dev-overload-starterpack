A. Simple for loop, prints 0 to 4

```
for i := 0; i < 5; i++ {
    fmt.Println(i)
}
```

B. Initializing Multiple values

```
for i, j := 0, 0; i < 5; i, j = i+1, j+1 {
    fmt.Println(i, j)
}
```

C. Initializer outside for block

```
count := 0
for ; count < 5; count++ {
    fmt.Println(count)
}
```

D. Do while for loop

```
num := 0
for num < 10 {
    fmt.Println(num)
    num = num + 2
}
```

E. Breaking an infinite loop

```
i := 0
for {
    fmt.Println("Execute me!")
    i++
    if i == 5 {
        break
    }
}
```

F. Using Continue statements

```
for i := 0; i < 10; i++ {
    if i%2 == 0 {
        continue
    }
    fmt.Printf("Prints even number: %v\n", i)
}
```

G. Breaking nested loop using Label

```
LoopLabel:
	for i := 1; i <= 3; i++ {
		for j := 1; j <= 3; j++ {
			// we want to exit the entire loop
			if i == 2 {
				// break - exits closes enclosing loop
				fmt.Println("Exiting...")
				break LoopLabel
			}
		}
	}
```

H. Looping collections

1. Array

```
s := [3]int{1, 2, 3}

for k, v := range s {
    fmt.Println(k, v)
}
```

2. Map

```
m := map[string]int{
    "a": 1,
    "b": 2,
    "c": 3}
for k, v := range m {
    fmt.Println(k, v)
}
```
