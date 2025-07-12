A. map[< key type >]< value type >{}

```go
countryPopulations := map[string]int{
    "countryA": 100,
    "countryB": 200,
    "countryC": 300,
}
fmt.Println(countryPopulations) // map[countryA:100 countryB:200 countryC:300]
```

B. instantiating the map without values

```go
options := make(map[string]string)
fmt.Println(options) // map[]
```

C. Using maps

```go
options = map[string]string{
    "a": "option A",
    "b": "option B",
}
fmt.Println(options["a"]) // Option A
```

D. Adding other key

```go
options["c"] = "option C"
fmt.Println(options["c"]) // Option C
```

E. Deleting value

```go
delete(options, "a")
```

F. Checking if value exists

```go
value, ok := options["b"]
fmt.Println(value, ok) // option B true
value, ok = options["a"]
fmt.Println(value, ok) //   false
```

G. Maps are copied by reference

```go
options2 := options
fmt.Println(options2) // map[b: option c:option C]
```
