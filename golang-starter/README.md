### The basics of Go

#### Tables of contents:

A. Sample apps

- [basic web app](go-wiki)

- [queue](queue)

B. Fundamentals:

- [arrays](go-basics/arrays.md)

- [channels](go-basics/channels.md)

- [concurrency](go-basics/concurrency.go)

- [constants](go-basics/constants.md)

- [defer](go-basics/defer.md)

- [functions](go-basics/functions.md)

- [goroutines](go-basics/goroutines.md)

- [if](go-basics/if.md)

- [interface](go-basics/interface.md)

- [loops](go-basics/loops.md)

- [map](go-basics/map.md)

- [panick](go-basics/panick.md)

- [pointers](go-basics/pointers.md)

- [primitives](go-basics/primitives.md)

- [slice](go-basics/slice.md)

- [struct](go-basics/struct.md)

- [switch](go-basics/switch.md)

- [variables](go-basics/variables.md)

#### A. Setup:

1.  Dowload go binary : https://golang.org/dl/

2.  Setup paths:

    GOROOT - path to go folder

    GOPATH - path where your go packages will be downloaded

3.  Add bin folders to path:

    PATH=$PATH:$GOROOT/bin

    PATH:$PATH:$GOPATH/bin

#### B. Workspace

Folder structures:

B1. Using your own package with go modules
    workspace/
        your/
            path/
                packagename/
                    example.go
    bin/
    main.go
    go.mod

1. Issue command `go build` on _working dir_ to build your app

2. Initialize `go.mod` file with: `go mod init module/path/here`

3.  Set built _binary_ path directory to your `bin/` folder:

        go env -w GOBIN=`pwd`/bin

        or

        export GOBIN=path/to/bin

4. `go install` to create binary file in `bin/` folder

5. Importing

_go.mod sample file_

    module module/name

    go 1.13

_main.go sample file_

    import module/name/packagename

_Important Notes_

1. Go **looks for the directory** where the dependencies are **installed** - this is the **GOPATH** directory.

2. If it is not present in **GOPATH**, go tries to download the module using the module/name/packagename.

3. By convention modules accesible on github is named: _github.com/module/packagename_

4. If you have a local module and you want to **import local package**. Your _go.mod_ may look like this:

```
module module/name

require (
    "some-dependency"
)
replace module/name/packagename =>  ./packagedir
```

#### C. Using go modules to automatically download dependencies

Example: main.go

```
import github.com/some/module
```

`go install` and `go build` will automatically handle dependencies

go.mod file will be:

```
module path/to/module

go 1.13

require github.com/some/module some.version

```

#### D. Everything in the same package will be automatically visible to the others in the same package

#### E. Delete downloaded modules:

    go clean -modcache

#### F. Remove unused package/s:
    
    go mod tidy

#### G. Building single binary

`CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o <binary-name> <root-folder-of-your-go-module>`

```

**References**:

Go web application: https://golang.org/doc/articles/wiki/

Go basics: https://www.youtube.com/watch?v=YS4e4q9oBaU

Go concurrency: https://www.youtube.com/watch?v=f6kdp27TYZs
```
