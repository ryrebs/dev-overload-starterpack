A. Struct - Collection of data , struct are copied by value

B. Creating struct

```go
type animal struct {
	sound  string
	count  int
	origin []string
}
```

C. Instantiating

```go
dog := animal{
    sound: "barks",
    count: 1,
    origin: []string{
        "country 1",
        "country 2",
    },
}
fmt.Println(dog)           // {barks 1 [country 1 country 2]}
fmt.Println(dog.sound)     // barks
fmt.Println(dog.origin[0]) // country 1
```

D. Composition / Embedding

```go
type cat struct {
	animal
	owner string
}
```

E. Tags

```go
import (
	"reflect"
)

type info struct {
	name             string `required max:"100"`
	expirationInDays int
}

info1 := info{
    name:             "puffy",
    expirationInDays: 1}
fmt.Println(info1) // {puffy 1}

t := reflect.TypeOf(info{})
field, ok := t.FieldByName("name")
fmt.Println(field.Tag, ok) // required max: "100" true
```

F. Anonymous struct

```go
person := struct {
    name string
    age  int
}{
    name: "rods",
    age:  1,
}
fmt.Println(person) // { rods 1}
```
