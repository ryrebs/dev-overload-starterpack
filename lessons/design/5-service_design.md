# 🧠 Designing Robust APIs: REST, RPC, Communication & Failure Handling

---

# 2. Who This Is For

- Intermediate engineers building APIs or microservices
- Familiar with:
  - HTTP basics
  - backend systems

---

# 3. Problem Definition

### Real-world scenario

You are building a backend system:

```
Mobile App → API → Services → DB
```

---

### Requirements

- clean API design
- scalable communication
- reliable under failures
- secure access

---

### Example

```
GET /users/123
POST /orders
```

---

### Constraints

- latency < 100ms
- services distributed
- partial failures happen
- evolving API over time

---

### Core Problem

👉 **How do we design APIs that are clear, scalable, and resilient?**

---

# 🧠 4. First Principles Thinking

---

## Why does this problem exist?

Because:

👉 Systems communicate over networks  
👉 Networks are unreliable  
👉 APIs evolve over time  

---

## What breaks without good design?

```
Confusing APIs
Tightly coupled services
Frequent failures
```

---

## Naive System

```
Client → API → Service → DB
```

---

## Failure Scenario

```
Client → API → Service ❌ (timeout)
```

---

## Why it fails

- no structure
- no failure handling
- no versioning

---

# 🧭 5. Build the Intuition (Step-by-Step)

---

## Step 1 — API Design (Resource Modeling)

---

### Idea

Model system as resources

---

### Bad Design

```
GET /getUserData
POST /createUserNow
```

---

### Good Design

```
GET /users/123
POST /users
```

---

### Diagram

```
Resource:
User → /users/{id}
```

---

### Insight

👉 APIs should represent nouns, not actions

---

---

## Step 2 — REST Concepts

---

### Principles

- stateless
- resource-based
- standard HTTP methods

---

### Diagram

```
GET    → read
POST   → create
PUT    → update
DELETE → remove
```

---

### Flow

```
Client → HTTP → API → Resource
```

---

### Visualization

```
Client
 ↓
[GET /users/1]
 ↓
Server → response
```

---

---

## Step 3 — RPC / gRPC (When to Use)

---

### Problem

REST can be verbose

---

### RPC Approach

```
Client → call function → Server
```

---

### Diagram

```
Client → getUser() → Server
```

---

### gRPC

- binary protocol
- faster
- strongly typed

---

### Use RPC WHEN:

✔ internal services  
✔ high performance needed  

---

### Visualization

```
Service A → Service B (direct call)
```

---

---

## Step 4 — API Versioning

---

### Problem

APIs evolve

---

### Without versioning

```
Change API → break clients ❌
```

---

### With versioning

```
/v1/users
/v2/users
```

---

### Diagram

```
Client → v1 → stable
Client → v2 → new features
```

---

### Insight

👉 backward compatibility

---

---

## Step 5 — Authentication vs Authorization

---

### Authentication (Who?)

```
User proves identity
```

---

### Authorization (What?)

```
User allowed actions
```

---

### Diagram

```
Request
 ↓
Auth (who?)
 ↓
AuthZ (allowed?)
```

---

---

## Step 6 — Service-to-Service Communication

---

### Problem

Services need to talk

---

### Sync

```
Service A → Service B
```

---

### Async

```
Service A → Queue → Service B
```

---

### Diagram

```
A → HTTP → B
A → Queue → B
```

---

### Insight

👉 choose based on latency vs decoupling

---

---

## Step 7 — Timeouts & Retries

---

### Problem

Requests hang

---

### Timeout

```
Request → wait → fail after limit
```

---

### Retry

```
Fail → retry → success
```

---

### Diagram

```
Request → Service
         ↓
      timeout
         ↓
       retry
```

---

### Insight

👉 prevents infinite waiting

---

---

## Step 8 — Circuit Breaker

---

### Problem

Failing service causes cascade

---

### Without Circuit Breaker

```
Service A → Service B ❌ (keeps trying)
```

---

### With Circuit Breaker

```
Failure threshold reached → stop calls
```

---

### Diagram

```
A → [Circuit Breaker] → B
         ↓
     open (stop)
```

---

### States

- closed (normal)
- open (blocked)
- half-open (testing)

---

# 🧠 6. Mental Model

---

## API Stack

```
Client
 ↓
API (REST / RPC)
 ↓
Auth → AuthZ
 ↓
Service communication
 ↓
DB
```

---

## Failure Handling

```
Timeout → Retry → Circuit Breaker
```

---

## Before vs After

---

### Before

```
Client → Service → failure ❌
```

---

### After

```
Client → Timeout → Retry → Circuit Breaker ✔
```

---

# 🏗️ 7. Final System Design

---

## System Diagram

```
           ┌──────────┐
           │  Client  │
           └────┬─────┘
                ▼
        ┌──────────────┐
        │   API Layer  │
        └────┬─────────┘
             ▼
     ┌──────────────┐
     │ Auth/AuthZ   │
     └────┬─────────┘
             ▼
     ┌──────────────┐
     │ Service A    │
     └────┬─────────┘
             ▼
     ┌──────────────┐
     │ Circuit Brkr │
     └────┬─────────┘
             ▼
     ┌──────────────┐
     │ Service B    │
     └──────────────┘
```

---

## Request Flow

```
1. Client calls API
2. Auth check
3. API routes to service
4. Service calls downstream
5. Apply timeout/retry
6. Circuit breaker protects system
```

---

## Data Flow

```
Request → Validation → Processing → Response
```

---

# 🔧 8. Implementation Perspective

---

## Technologies

- REST: HTTP/JSON
- gRPC: Protobuf
- Auth: JWT / OAuth
- Circuit breaker: Hystrix / Resilience4j

---

## Pseudo Flow

```
callService():
    try:
        response = service.call(timeout=100ms)
    except:
        retry()

    if failures > threshold:
        open_circuit()
```

---

# 🧪 9. Walkthrough Example

---

### Request: GET /users/123

---

### Steps

```
1. Client sends request
2. Auth verified
3. API routes to user service
4. Service calls DB
5. Response returned
```

---

### Failure Case

```
Service fails → retry → circuit breaker opens
```

---

### Visual Trace

```
Client
 ↓
API
 ↓
Service
 ↓
DB
```

---

# ⏱️ 10. Performance & Scalability

---

## Bottleneck

```
Slow service → blocks system ❌
```

---

## With Resilience

```
Timeout + retry + circuit breaker ✔
```

---

## Diagram

```
Failure → isolated
```

---

# ⚖️ 11. Tradeoffs and Alternatives

---

## REST vs RPC

```
REST:
Flexible, readable

RPC:
Fast, efficient
```

---

## Diagram

```
REST → HTTP resource
RPC  → function call
```

---

# ⚠️ 12. Common Mistakes

---

## 1. No versioning

```
Breaking clients ❌
```

---

## 2. No timeouts

```
Requests hang forever ❌
```

---

## 3. No circuit breaker

```
Failures cascade ❌
```

---

## Broken System

```
Service A → Service B → crash
```

---

# 🌍 13. Real-World Usage

- Google APIs (REST + gRPC)
- Netflix (circuit breakers)
- Stripe (clean API design)

---

# 🚀 14. Variations and Extensions

---

## GraphQL

```
Client specifies fields
```

---

### Diagram

```
Client → GraphQL → data
```

---

## API Gateway Pattern

```
Client → Gateway → services
```

---

# 🔁 15. Recap (Feynman Compression)

👉 Good APIs:

- model resources clearly
- choose REST or RPC wisely
- version properly
- secure with auth/authz
- handle failures (timeout, retry, circuit breaker)

---

# 🧩 16. Exercises

---

### Easy

1. Why use resource-based APIs?
2. Difference between auth and authorization?

---

### Intermediate

3. Design API for:
   - user + orders
   - versioning support

---

### Real-World Challenge

4. Design system for:

- multiple services
- high reliability
- evolving API

👉 Include:
- REST vs RPC decision
- retries
- circuit breaker