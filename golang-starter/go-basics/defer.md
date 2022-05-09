A. Defer - executes a function before the main function returns

```
// Executes in LIFO
fmt.Println("start")
defer fmt.Println("middle")
fmt.Println("end")
// start
// end
// middle
```

B. Closing a resource before function returns

```
    import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)
	res, err := http.Get("http://www.google.com/robots.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer res.Body.Close()
	robots, err := ioutil.ReadAll(res.Body)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("%s", robots)
```

C. Defer process variables at the time it is called

```
a := "start"
fmt.Println(a)
a = "end"
// start
```
