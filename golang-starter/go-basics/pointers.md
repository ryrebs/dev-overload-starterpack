A. Pointer - contains the address in memory of the variable being pointed at.

```
value := 1
p2Value := &value // var p2Value *int = &value
fmt.Println(value, p2Value)
// 1 0xc00001c0d8

fmt.Println(value, *p2Value)
// 1 1.
```

B. Pointer arithmetic - `this is not supported` unless / might be through `unsafe` package

```
a := [3]int{1, 2, 3}
b := &a[0]
c := &a[1]                       // - 4 (subtracting 4 will not point to a[0])
fmt.Printf("%v %p, %p", a, b, c) // value, pointer, pointer
// values are 4 bytes away
// [1 2 3] 0xc00001e400, 0xc00001e408
```

C. new(T) - use to allocate _zeroed storage/memory_ of type T and returns its address. **Does not** *initialize it*.

```
type myStruct struct {
    foo int
}
var ms *myStruct
ms = new(myStruct)
(*ms).foo = 1 // same as ms.foo = 1
fmt.Println(ms) // &{1}
fmt.Println(ms.foo) // 1
fmt.Println(*ms) // {1} 

```
