A. Interface - collection of function signatures; describes _behavior_ unlike _struct_ which describes data

B. Naming convention should be _method name_ + _er_

```
func main() {
	// create variable of type Writer
	var w Writer = ConsoleWriter{}
	w.Write([]byte("Hello Go!"))
}

type Writer interface {
	// describe the method signature
	Write([]byte) (int, error)
}


```

B.1. Implicitly implements the Writer interface by creating the method signature _Write_

```
type ConsoleWriter struct{}

func (vw ConsoleWriter) Write(data []byte) (int, error) {
	n, err := fmt.Println(string(data))
	return n, err
}
```

C. Using custom type other than struct

```
func main() {
	myInt := myInt(10)
	var doubled incrementer = &myInt
	fmt.Printf("%v\n", myInt)            // 10
	fmt.Printf("%v\n", doubled.Double()) // 20
	fmt.Printf("%v", doubled.Double())   // 40

}

type incrementer interface {
	Double() int
}

type myInt int

func (ic *myInt) Double() int {
	*ic = *ic * 2
	return int(*ic)
}
```

D. Creating interface with more than one methods

```
func main() {

	var wc writerCloser = newBufferedWriterCloser() // Call the constsructor
	wc.Write([]byte("I am testing buffers"))
	wc.Close()
	// wc.buffer is not accessible
	// writerCLoser is not aware of the implementation of bufferedWriterCloser

	// type conversion with error handling to avoid panic
	bwc, ok := wc.(*bufferedWriterCloser)
	if ok {
		fmt.Println("Buffer: ", bwc.buffer) // buffer is now accessible
	} else {
		fmt.Println("Convertion failed")
	}

}

// interfaces
type writer interface {
	Write([]byte) (int, error)
}

type closer interface {
	Close() error
}

// combined interfaces
type writerCloser interface {
	writer
	closer
}

type bufferedWriterCloser struct {
	buffer *bytes.Buffer
}

// implement the write method
func (bwc *bufferedWriterCloser) Write(data []byte) (int, error) {
	n, err := bwc.buffer.Write(data)
	if err != nil {
		return 0, err
	}

	v := make([]byte, 8)
	// read and print only 8 characters
	for bwc.buffer.Len() > 8 {
		_, err := bwc.buffer.Read(v)
		if err != nil {
			return 0, err
		}
		_, err = fmt.Println(string(v))
		if err != nil {
			return 0, err
		}
	}
	return n, nil
}

// implement the close method
func (bwc *bufferedWriterCloser) Close() error {
	// read the next n bytes from the buffer
	// else return all bytes if n < buffer length
	for bwc.buffer.Len() > 0 {
		data := bwc.buffer.Next(8)
		_, err := fmt.Println(string(data))
		if err != nil {
			return err
		}
	}
	return nil
}

// constructor
func newBufferedWriterCloser() *bufferedWriterCloser {
	return &bufferedWriterCloser{
		buffer: bytes.NewBuffer([]byte{}),
	}
}

// Output with close()
/**
I am tes
ting buf
fers
*/

// Output without close()
/** I am tes
ting buf
*/
```

E. Using an empty interface

```
var myObj interface{} = newBufferedWriterCloser()
// type cast the empty interface
if wc, ok := myObj.(writerCloser); ok {
	wc.Write([]byte("I am testing buffers"))
	wc.Close()
}
```

F. Using empty interface on switch to check for data type

```
var i interface{} = 1
switch i.(type) {
case int:
    fmt.Println("int")
    break // exit early
    fmt.Println("This will not print")
case float64:
    fmt.Println("float64")
default:
    fmt.Println("Invalid type")
} // int
```

G. Pointer receiver vs value receiver.

If using a value receiver then you can initialize using a value or using the address

```
var wc writerCloser = writerCloser()
var wc2 writerCloser = &writerCloser()


type writer interface {
	Write([]byte)(int, error)
}


type closer interface {
	Closer() error
}

type writerCloser struct{
	writer
	closer
	}

type myWriterCloser struct{}

func (wc writerCloser) Write(data []byte) (int, error) {
	return 0, nil
}

func (wc writerCloser) Close() error {
	return nil
}
```

If receiver uses any pointer then initialize using the address

```
var wc2 writerCloser = &writerCloser()

func (wc *writerCloser) Write(data []byte) (int, error) {
	return 0, nil
}
```
