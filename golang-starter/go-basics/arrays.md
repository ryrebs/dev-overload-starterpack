A. Array with specifc size

```
// [size]type
grades := [3]int{1, 2, 3}
fmt.Println(grades) // [1 2 3]
```

B. Without specifying the size

```
// [...]type
grades2 := [...]int{1, 2, 3, 4}
fmt.Println(grades2) // [1 2 3 4]
```

C. Empty array and assigning value later

```
var students [3]string
fmt.Println(students) // []
students[0] = "student1"
fmt.Println(students) // [student1]
fmt.Println(len(students)) // 3
```

D. Arrays are copied by value

```
a := [...]int{1, 2, 3}
b := a
b[1] = 200
fmt.Println(a) // [1 2 3]
fmt.Println(b) // [1 200 3]
```

E. Using pointers to access a reference to array's memory address

```
a := [...]int{1, 2, 3}
b := &a
b[1] = 200
fmt.Println(a) // [1 200 3]
fmt.Println(*b) // [1 200 3]
```

**Array vs Slice:**

    Array:
    [...]int{1,2,3}
    [3]int{1,2,3}

    Slice:
    make([]int, 3, 100)
    []int{1,2,3}