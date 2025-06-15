# Go REST API Refresher Course

A step‑by‑step guide from basics to advanced topics, with real code examples and the reasoning behind each pattern.

---

## 1. Getting Started

1. **Install Go** (version ≥ 1.20):  
   Download from https://go.dev/dl and follow the installer for your OS.

2. **Workspace & Modules**

   - Create a project folder and enter it:
     ```bash
     mkdir ~/projects/myapi
     cd ~/projects/myapi
     ```
   - Initialize a module (dependency manifest):
     ```bash
     go mod init github.com/you/myapi
     ```
   - This creates `go.mod`, which tracks your module path and versions.

3. **Go Toolchain**
   - `go build` → compile
   - `go run .` → build & run
   - `go test ./...` → run tests
   - `go fmt ./...` → format code
   - `go vet ./...` → static checks
   - `go mod tidy` → clean unused dependencies

---

## 2. Core Language Fundamentals

### 2.1 Variables & Types

```go
var count int = 5         // explicit type
name := "Go Developer"    // type inferred
const Pi = 3.14159        // constant (immutable)
Why:

// Use var when clarity matters (public APIs, libraries).

// Use := for brevity in local code.

// const prevents accidental reassignment.
```

### 2.2 Composite Types

```go
scores := []int{100, 95, 80} // slice: dynamic array
roles := map[string]string{"u1":"admin"} // map: fast lookups

type User struct { // struct: custom type
ID int
Name string
}
u := User{ID:1, Name:"Alice"} // instantiate

// Why:

// Slices grow/shrink easily.

// Maps provide O(1) key‑value access.

// Structs model domain entities.
```

```go

// Loop and condition
for i, s := range scores {
if s < 90 {
fmt.Printf("score %d is below 90\n", i)
}
}

// Switch without fall‑through by default
switch u.Name {
case "Alice":
fmt.Println("Welcome back, Alice")
default:
fmt.Println("Hello guest")
}
Why:

// Single for handles all looping needs.

// switch defaults to no fall‑through to avoid mistakes.
```

### 3. Modules & Package Organization

```
3.1 Project Layout
   csharp
   Copy
   Edit
   myapi/
   ├── go.mod
   ├── cmd/
   │ └── server/ # main entrypoint
   │ └── main.go
   ├── internal/ # private packages
   │ └── store/
   │ └── memstore.go
   └── pkg/ # reusable packages
   └── api/
   └── handler.go
```

Why:

1. cmd/ holds executables.
2. internal/ prevents public imports.
3. pkg/ for code shared externally or between services.

### 3.2 Dependency Management

```bash
go get github.com/go-chi/chi@latest # add router
go get github.com/go-playground/validator # add validator
go mod tidy # remove unused deps 4. Error Handling & Logging
```

### 4.1 Errors

```go
func divide(a, b float64) (float64, error) {
if b == 0 {
return 0, fmt.Errorf("divide by zero")
}
return a / b, nil
}

result, err := divide(10, 0)
if err != nil {
log.Printf("divide error: %v", err)
}
// Why:
// Propagate errors explicitly.
// Avoid panics for predictable failures.
```

### 4.2 Wrapping & Unwrapping

```go
func readFile(path string) error {
_, err := os.ReadFile(path)
return fmt.Errorf("read %s: %w", path, err)
}

err := readFile("nofile.txt")
if errors.Is(err, fs.ErrNotExist) {
fmt.Println("file not found")
}
// Why:
// %w wrapping lets callers detect underlying causes with errors.Is or errors.As.
```

### 4.3 Logging

```go
logger := zap.NewExample() // structured logger
defer logger.Sync()
logger.Info("starting server", zap.String("port", "8080"))
// Why:
// Structured logs (JSON) are easier to query in production.
```

### 5. Context & HTTP Basics

#### 5.1 Context

```go
func fetch(ctx context.Context, url string) ([]byte, error) {
  req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)
  resp, err := http.DefaultClient.Do(req)
if err != nil {
return nil, err
}
defer resp.Body.Close()
return io.ReadAll(resp.Body)
}

ctx, cancel := context.WithTimeout(context.Background(), 2\*time.Second)
defer cancel()
data, err := fetch(ctx, "https://example.com")
// Why:
// context propagates deadlines, cancellations, and request‑scoped values.
```

#### 5.2 net/http Handler

```go
http.HandleFunc("/health", func(w http.ResponseWriter, r \*http.Request) {
w.WriteHeader(http.StatusOK)
w.Write([]byte("OK"))
})
log.Fatal(http.ListenAndServe(":8080", nil))
// Why:
// Built‑in server is zero‑config to get started quickly.
```

### 6. Middleware & Routing

#### 6.1 Chi Router

```go
r := chi.NewRouter()
r.Use(middleware.Logger) // logs requests
r.Use(middleware.Recoverer) // recovers panics

r.Post("/users", createUserHandler)
log.Fatal(http.ListenAndServe(":8080", r))
// Why:
// Router frameworks simplify URL patterns and middleware chains.
```

#### 6.2 Custom Middleware

```go
func auth(next http.Handler) http.Handler {
return http.HandlerFunc(func(w http.ResponseWriter, r \*http.Request) {
token := r.Header.Get("Authorization")
if token != "secret" {
http.Error(w, "unauthorized", 401)
return
}
next.ServeHTTP(w, r)
})
}

r.Use(auth)
// Why:
// Middleware decouples cross‑cutting concerns (auth, logging, metrics).
```

### 7. Validation & Configuration

#### 7.1 Request Validation

```go
   type Signup struct {
   Email string `validate:"required,email"`
   Age int `validate:"gte=18"`
   }

validate := validator.New()
var in Signup
json.NewDecoder(r.Body).Decode(&in)
if err := validate.Struct(in); err != nil {
http.Error(w, err.Error(), 400)
return
}
// Why:
// Struct tags declare rules; library enforces them automatically.
```

#### 7.2 Configuration

```go
type Config struct {
Port string `env:"PORT,default=8080"`
}
var cfg Config
envconfig.Process("", &cfg)
// Why:
// 12‑factor apps read config from environment variables.
```

### 8. Concurrency Patterns

#### 8.1 Goroutines & Channels

```go
ch := make(chan int)
go func() {
// background work
ch <- 42
}()
result := <-ch
// Why:
// Lightweight threads + typed pipes for safe communication.
```

#### 8.2 Worker Pool

```go
tasks := make(chan int)
results := make(chan int)

for i := 0; i < 5; i++ {
go func() {
for n := range tasks {
results <- fib(n)
}
}()
}

for i := 0; i < 10; i++ {
tasks <- i
}
close(tasks)

for i := 0; i < 10; i++ {
fmt.Println(<-results)
}
// Why:
// Controls concurrency to avoid overloading CPU or I/O.
```

### 9. Design Patterns & Architecture

#### 9.1 Dependency Injection

```go
type UserRepo interface {
Save(User) error
}

type Service struct {
Repo UserRepo
}

func NewService(r UserRepo) \*Service {
return &Service{Repo: r}
}
// Why:
// Pass dependencies in constructors for testability and decoupling.
```

#### 9.2 Clean Architecture Layers

- Entities (core types)

- Use Cases (business rules)

- Adapters (HTTP handlers, DB)

- Frameworks/Drivers (main, routers)

Why:
Separates concerns and shields core logic from external changes.

### 10. Testing & Quality

#### 10.1 Unit Tests

```go
func TestAdd(t \*testing.T) {
if got := Add(2, 3); got != 5 {
t.Errorf("Add(2,3) = %d; want 5", got)
}
}
// Why:
// Fast feedback and confidence when refactoring.
```

#### 10.2 Table‑Driven Tests

```go
tests := []struct {
in []int
want []int
}{
{[]int{1, 2, 3}, []int{3, 2, 1}},
{[]int{}, []int{}},
}
for \_, tc := range tests {
if got := Reverse(tc.in); !reflect.DeepEqual(got, tc.want) {
t.Errorf("Reverse(%v) = %v; want %v", tc.in, got, tc.want)
}
}
// Why:
// Scales easily to many scenarios with minimal code duplication.
```

#### 10.3 Fuzz Testing

```go
func FuzzReverse(f *testing.F) {
f.Add("radar")
f.Fuzz(func(t *testing.T, s string) {
if rev(reverse(s)) != s {
t.Errorf("mismatch %q", s)
}
})
}
// Why:
// Discovers edge‑case bugs automatically.
```

### 11. Performance & Profiling

#### 11.1 pprof

```go
import _ "net/http/pprof"

func main() {
go http.ListenAndServe(":6060", nil)
// your API server...
}
// Why:
// Exposes CPU/memory profiles to diagnose bottlenecks.
```

#### 11.2 Benchmarking

```go

func BenchmarkJoin(b \*testing.B) {
for i := 0; i < b.N; i++ {
_ = strings.Join([]string{"a", "b"}, "")
}
}
// Why:
// Measures performance to guide optimizations.
```

### 12. Security Best Practices

- HTTPS: Always serve TLS (Let’s Encrypt + certmagic).
- Input Sanitization: Validate all user inputs before use.
- Authentication & Authorization: JWT, OAuth2, or session tokens with proper middleware.
- Rate Limiting: golang.org/x/time/rate to prevent abuse.
- Secrets Management: Never hard‑code; use environment variables or vaults.

### 13. Deployment & Observability

#### 13.1 Docker Multi‑Stage

```dockerfile
FROM golang:1.20 AS builder
WORKDIR /app
COPY . .
RUN go mod tidy && go build -o server ./cmd/server

FROM alpine:latest
COPY --from=builder /app/server /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/server"]
# Why:
# Produces minimal, secure container images.
```

#### 13.2 Metrics & Tracing

```go
import "github.com/prometheus/client_golang/prometheus/promhttp"

http.Handle("/metrics", promhttp.Handler())
// Why:
// Prometheus‑compatible metrics for monitoring.
// For distributed tracing, integrate OpenTelemetry and propagate spans through HTTP handlers.
```

## Go Advanced Refresher Course with In‑Depth Explanations and Examples

This guide not only shows you idiomatic Go code but explains **why** each pattern matters, so you understand both the implementation and its purpose.

---

### 1. Language Fundamentals (Recap with Rationale)

#### Variable Declaration

```go
var x int = 42          // declaring x explicitly as int
y := "hello, Go"       // shorthand: compiler infers string type
const Pi = 3.14159      // immutable constant for mathematical accuracy
```

- **Why**: Explicit types (`var`) improve readability in libraries; shorthand (`:=`) speeds up local code. Constants guard against accidental modification.

#### Composite Types

```go
scores := []int{100, 95, 80}               // slice: dynamically-sized array
userRoles := map[string]string{"u1":"admin"}  // map: key->value lookup

type User struct { ID int; Name string }   // struct: grouping related fields
u := User{ID:1, Name:"Alice"}             // instantiate User struct
```

- **Why**: Slices allow flexible collections; maps provide O(1) lookups; structs model domain entities.

#### Control Flow

```go
for i, s := range scores {
  // range loop iterates with index i and value s
  if s < 90 {
    fmt.Printf("score %d is below 90\n", i)
  }
}

switch u.Name {
case "Alice": fmt.Println("Hi Alice")
default:       fmt.Println("Hello guest")
}
```

- **Why**: Go’s single `for` handles all loops for simplicity. `switch` without fall-through prevents unintentional cases.

---

### 2. Interfaces & Implicit Implementation

Interfaces let you write **decoupled** code: functions depend on behaviors, not concrete types.

#### Built‑in Reader Example

```go
// Reader defines a Read method: any type with Read satisfies it.
type Reader interface { Read(p []byte) (n int, err error) }

// bytes.Buffer implements Read internally.
var r Reader = bytes.NewBufferString("data")
buf := make([]byte, 4)
n, err := r.Read(buf)
if err != nil { log.Fatal(err) }
fmt.Println(string(buf[:n]))  // prints "data"
```

- **Why**: By coding to `Reader`, you can swap in files, network streams, or buffers without changing client code.

#### Custom Store Interface

```go
type Store interface {
  Save(key string, value []byte) error
  Load(key string) ([]byte, error)
}

type MemStore map[string][]byte

// MemStore implicitly implements Store by defining Save and Load
func (m MemStore) Save(k string, v []byte) error { m[k] = v; return nil }
func (m MemStore) Load(k string) ([]byte, error) {
  v, ok := m[k]
  if !ok { return nil, fmt.Errorf("key %s not found", k) }
  return v, nil
}

// Use Store abstraction
var s Store = MemStore{}
err := s.Save("foo", []byte("bar"))
val, _ := s.Load("foo")
fmt.Println(string(val))  // prints "bar"
```

- **Why**: You can replace `MemStore` with a database-backed implementation without touching higher-level code.

---

### 3. Generics (Type Safety + Reusability)

Go generics let you write **one** function that works for **many** types while preserving compile-time safety.

#### Generic Map Function

```go
func Map[T any](items []T, fn func(T) T) []T {
  res := make([]T, len(items))  // allocate result slice of same type
  for i, v := range items {
    res[i] = fn(v)
  }
  return res
}

// Double each element in an []int:
doubled := Map([]int{1,2,3}, func(x int) int { return x * 2 })
fmt.Println(doubled)  // [2 4 6]
```

- **Why**: Avoids writing separate `MapInts`, `MapStrings`, etc., yet errors if you misuse types.

#### Constrained Sum Function

```go
type Number interface { ~int | ~float64 }

func Sum[T Number](a, b T) T { return a + b }

fmt.Println(Sum(1, 2), Sum(1.5, 2.5))  // 3 4.0
```

- **Why**: `~int` allows all named types underlying `int`, giving flexibility while preventing unsupported types.

---

### 4. Concurrency & Patterns

Concurrency is a Go strength. Use goroutines for parallelism, channels for coordination.

#### Simple Goroutine & Channel

```go
func fibonacci(n int) int {
  if n < 2 { return n }
  return fibonacci(n-1) + fibonacci(n-2)
}

ch := make(chan int)
go func() { ch <- fibonacci(6) }()  // compute in background
d := <-ch                                // wait for result
fmt.Println("fib(6) =", d)
```

- **Why**: Non-blocking launch with `go`; channel `<-` synchronizes and transfers data safely.

#### Worker Pool Pattern

```go
tasks := make(chan int, 5)
results := make(chan int, 5)

// Start 3 workersor w := 0; w < 3; w++ {
  go func(id int) {
    for t := range tasks {
      results <- t * t  // square the number
    }
  }(w)
}

// Send 5 tasks
for i := 0; i < 5; i++ { tasks <- i }
close(tasks)

// Collect results
for i := 0; i < 5; i++ {
  fmt.Println(<-results)
}
```

- **Why**: Spawns fixed-number workers to process tasks from a channel, limiting parallelism and avoiding resource exhaustion.

#### Context Cancellation

```go
func fetch(ctx context.Context, url string) ([]byte, error) {
  req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)
  resp, err := http.DefaultClient.Do(req)
  if err != nil { return nil, err }
  defer resp.Body.Close()
  return io.ReadAll(resp.Body)
}

ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
 defer cancel()  // ensures resources freed

data, err := fetch(ctx, "https://example.com")
if err != nil {
  log.Println("fetch error:", err)
} else {
  fmt.Println("received", len(data), "bytes")
}
```

- **Why**: Propagates timeouts or cancellations so that HTTP requests don’t hang indefinitely.

---

### 5. Reflection & `unsafe`

Use reflection sparingly for dynamic behaviors; `unsafe` only for performance-critical or low-level code.

#### Reflection: Automatic Field Printer

```go
func PrintFields(i interface{}) {
  v := reflect.ValueOf(i)
  t := v.Type()
  for j := 0; j < v.NumField(); j++ {
    name := t.Field(j).Name
    value := v.Field(j).Interface()
    fmt.Printf("%s = %v\n", name, value)
  }
}

type Point struct{ X, Y int }
PrintFields(Point{X:10, Y:20})
// Output: X = 10\nY = 20
```

- **Why**: Enables generic tooling (serializers, mappers) that work on any struct.

#### unsafe Pointer Conversion

```go
var x float64 = 3.14
ptr := unsafe.Pointer(&x)
bytes := *(*[8]byte)(ptr)
fmt.Printf("raw bytes = %v\n", bytes)
```

- **Why**: Reveals underlying memory representation—useful in serialization or interfacing with C code, but bypasses safety.

---

### 6. Advanced Error Handling

Structuring errors clearly improves debuggability and API design.

#### Wrapping & Unwrapping

```go
func readFile(name string) error {
  _, err := os.ReadFile(name)
  return fmt.Errorf("read %s: %w", name, err)
}

err := readFile("nofile.txt")
if errors.Is(err, fs.ErrNotExist) {
  fmt.Println("file does not exist")
}
```

- **Why**: `%w` wraps errors so callers can detect root causes with `errors.Is`.

#### Custom Error Types

```go
type ValidationError struct { Field, Problem string }
func (e ValidationError) Error() string {
  return fmt.Sprintf("%s: %s", e.Field, e.Problem)
}

func validateEmail(email string) error {
  if !strings.Contains(email, "@") {
    return ValidationError{Field:"Email", Problem:"missing @"}
  }
  return nil
}

if err := validateEmail("bad"); err != nil {
  var ve ValidationError
  if errors.As(err, &ve) {
    fmt.Println("Validation failed on", ve.Field)
  }
}
```

- **Why**: Typed errors let callers handle specific conditions (validation vs IO vs other).

---

### 7. Design Patterns & Architecture

Structuring code for maintainability and testability.

#### Adapter Pattern

```go
type OldLogger struct{}
func (l OldLogger) LogMsg(msg string) { fmt.Println("OLD:", msg) }

type Logger interface { Log(string) }

// Adapter wraps OldLogger to satisfy new Logger interface
func (l OldLogger) Log(s string) { l.LogMsg(s) }

func Process(log Logger) {
  log.Log("processing...")
}

Process(OldLogger{})  // no code change needed to integrate legacy logger
```

- **Why**: Allows integrating incompatible APIs without rewriting existing code.

#### Hexagonal Architecture (Ports & Adapters)

```go
// Domain port
 type UserRepo interface {
   Save(user User) error
 }

// Adapter for SQL implementation
type SQLRepo struct{ DB *sql.DB }
func (r *SQLRepo) Save(u User) error {
  _, err := r.DB.Exec("INSERT INTO users(name) VALUES(?)", u.Name)
  return err
}

// Application logic depends only on UserRepo interface
func RegisterUser(repo UserRepo, name string) error {
  return repo.Save(User{Name:name})
}

// Wiring together in main
func main() {
  db, _ := sql.Open("mysql", "dsn")
  repo := &SQLRepo{DB: db}
  _ = RegisterUser(repo, "Bob")
}
```

- **Why**: Decouples business rules from infrastructure, making code easier to test and evolve.

---

### 8. Building Robust REST APIs

Combining router frameworks, middleware, and validation for production readiness.

#### Chi Router with Middleware

```go
r := chi.NewRouter()
// Logging: records request method and path
github.com/go-chi/chi/middleware.Logger(r)
// Recoverer: prevents panics from crashing the server
github.com/go-chi/chi/middleware.Recoverer(r)

r.Post("/items", func(w http.ResponseWriter, r *http.Request) {
  var it Item
  if err := json.NewDecoder(r.Body).Decode(&it); err != nil {
    http.Error(w, "invalid JSON", http.StatusBadRequest)
    return
  }
  // Save to DB or in-memory store...
  w.WriteHeader(http.StatusCreated)
})

http.ListenAndServe(":8080", r)
```

- **Why**: Middlewares add cross-cutting concerns (logging, panic recovery) declaratively.

#### Request Validation

```go
type User struct {
  Name  string `json:"name" validate:"required,min=3"`
  Email string `json:"email" validate:"required,email"`
}

validate := validator.New()
r.Post("/users", func(w http.ResponseWriter, r *http.Request) {
  var u User
  _ = json.NewDecoder(r.Body).Decode(&u)
  if err := validate.Struct(u); err != nil {
    http.Error(w, err.Error(), http.StatusBadRequest)
    return
  }
  // proceed with u.Name and u.Email
})
```

- **Why**: Declarative struct tags centralize validation rules and reduce boilerplate.

---

### 9. Testing & Quality

Ensuring correctness and catching regressions.

#### Table‑Driven Tests

```go
tests := []struct { input []int; want []int }{
  {[]int{1,2,3}, []int{3,2,1}},
  {[]int{}, []int{}},
}
for _, tc := range tests {
  got := Reverse(tc.input)
  if !reflect.DeepEqual(got, tc.want) {
    t.Errorf("Reverse(%v) = %v; want %v", tc.input, got, tc.want)
  }
}
```

- **Why**: Scales easily to many cases and improves readability.

#### Fuzz Testing

```go
func FuzzIsPalindrome(f *testing.F) {
  f.Add("radar")
  f.Fuzz(func(t *testing.T, s string) {
    if IsPalindrome(s) && len(s) > 0 && s[0] != s[len(s)-1] {
      t.Errorf("contradiction for %s", s)
    }
  })
}
```

- **Why**: Automatically explores edge cases beyond your static test suite.

---

### 10. Performance & Profiling

Identifying and fixing bottlenecks.

#### pprof Integration

```go
import _ "net/http/pprof"
func main() {
  go http.ListenAndServe(":6060", nil)
  // your application logic...
}
```

- **Why**: Exposes runtime metrics (CPU, memory, goroutines) through HTTP endpoints for analysis.

#### Benchmarking

```go
func BenchmarkConcat(b *testing.B) {
  for i := 0; i < b.N; i++ {
    _ = strings.Join([]string{"a","b"}, "")
  }
}
```

- **Why**: Measures allocation and speed; guides optimization.

---

### 11. Tooling & Ecosystem

- **Linting**: `golangci-lint run` finds style and bug patterns early.
- **Formatting**: `go fmt ./...` enforces uniform code style.
- **Editor Support**: `gopls` in VSCode or GoLand for live errors and refactoring.

---

### 12. Deployment & Observability

#### Docker Multi-Stage

```dockerfile
FROM golang:1.20 AS builder
WORKDIR /app
COPY . .
RUN go mod tidy && go build -o /server ./cmd/server
FROM alpine
COPY --from=builder /server /usr/local/bin
ENTRYPOINT ["/usr/local/bin/server"]
```

- **Why**: Produces minimal container with only the static binary, reducing attack surface.

#### Prometheus Metrics

```go
import "github.com/prometheus/client_golang/prometheus/promhttp"

http.Handle("/metrics", promhttp.Handler())
go http.ListenAndServe(":9090", nil)
```

- **Why**: Standard interface for scraping application metrics for monitoring dashboards.

---

_This advanced guide combines practical code with explanations of why and when to use each feature, empowering you to write robust, idiomatic Go for high‑quality REST APIs._

```

```
