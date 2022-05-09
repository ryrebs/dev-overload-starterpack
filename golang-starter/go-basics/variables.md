A. Variables declared at package level should always have type

```
var pkgVar float32 = 1.2

//  Grouping variable declarations for organization
var (
	name string = "samsie"
	age  int    = 5
)
```

B. Naming:

1. lower case variables are scope to the package it belongs
2. upper case variables are scope globally
3. block scope are variables declared inside the function/block

   E.g
   var scopedHere string = ""
   var ScopedOutside string = ""

4. the shorter the life the shorter the name
5. Pascal or camelCase
6. all acronyms should be capitalize

C. Sample Codes

```
import (
	"fmt"
	"strconv"
)

func main() {
	// Declaring variables
	var i int
	i = 42
	var j int = 43
	k := 44 // go infers the type, // used inside function only
    var myHTTP string = "httpDemo"

	// Printing
	fmt.Println(i)             // 42
	fmt.Println(j)             // 43
	fmt.Println(k)             // 44
	fmt.Printf("%v, %T", j, j) // 43, int

	// Conversion
	var l float32
	l = float32(i)
	fmt.Printf("\nint 42 is converted to %v with type %T ", l, l)

	// convert properly to string ASCII not UNICODE
	var str string = strconv.Itoa(50)
	fmt.Println("\n" + str)
}

```
