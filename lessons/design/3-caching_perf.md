# 🧠 Designing High-Performance Systems: Caching, Rate Limiting & Load Control

---

# 2. Who This Is For

- Intermediate engineers (backend / systems)
- Basic knowledge of:
  - HTTP APIs
  - Databases
  - Latency concepts

---

# 3. Problem Definition

Modern systems must handle:

- millions of users
- low latency (<100ms)
- limited infrastructure

### Example

You run a product API:

```
GET /product/123
```

Each request hits the database.

---

### Constraints

- DB can handle: 5k QPS
- Traffic: 100k QPS
- Latency requirement: <50ms

---

### Problem

Without optimization:

- DB overload
- high latency
- system crashes

---

# 🧠 4. First Principles Thinking

### Why does this problem exist?

Because:

👉 **Data access is slow**  
👉 **Requests are redundant**

---

### What breaks?

```
        ┌─────────┐
Users → │  API    │ → DB
        └─────────┘
```

DB becomes bottleneck.

---

### Naive Flow

```
User A ─┐
User B ─┼──> API ───> DB
User C ─┘
```

---

### Why it fails

- Same data requested repeatedly
- DB does repeated work
- No reuse

---

# 🧭 5. Build the Intuition (Step-by-Step)

---

## Step 1 — Add Cache (Cache-Aside)

### Idea:

Check cache before DB.

---

### Flow

```
        ┌─────────┐
User →  │  API    │
        └────┬────┘
             │
      ┌──────▼──────┐
      │   Cache     │
      └──────┬──────┘
             │ miss
             ▼
            DB
```

---

### Behavior

```
if (cache.has(key)):
    return cache.get(key)
else:
    data = DB.get(key)
    cache.set(key, data)
    return data
```

---

## Step 2 — Write Strategies

---

### Write-Through

Write to cache + DB synchronously.

```
Client → API → Cache → DB
```

```
        ┌─────────┐
        │  API    │
        └────┬────┘
             ▼
         Cache
             ▼
             DB
```

✔ consistent  
❌ slower writes

---

### Write-Back (Write-Behind)

Write to cache first, DB later async.

```
Client → API → Cache → (async) DB
```

```
        ┌─────────┐
        │  API    │
        └────┬────┘
             ▼
          Cache
             │
         (async)
             ▼
             DB
```

✔ fast  
❌ risk of data loss

---

## Step 3 — Cache Invalidation (The Hard Part)

### Problem:

```
Cache: old value
DB:    new value
```

---

### Broken System

```
User updates DB
      │
      ▼
     DB (new)

Cache still has old data ❌
```

---

### Fix Options

#### 1. Delete on write

```
Write → DB
       → delete cache
```

---

#### 2. Update cache

```
Write → DB
       → update cache
```

---

### Visualization

```
Before:
Cache → v1
DB    → v1

After update:
Cache → v1 ❌
DB    → v2
```

---

## Step 4 — TTL Strategy

### Idea

Auto-expire cache.

---

### Flow

```
Cache Entry:
[ value | expires_at ]
```

---

### Diagram

```
Time →
|-----valid-----| expired |

cache hit       miss → DB
```

---

### Tradeoff

- Short TTL → fresh data, more DB load
- Long TTL → stale data, less DB load

---

## Step 5 — Hot Keys Problem

### Problem

One key gets massive traffic.

```
GET /product/1  ← 90% traffic
```

---

### Visualization

```
Requests:
[1][1][1][1][1][1][2][3]

Cache node overloaded ❌
```

---

### Solution: Replication / Sharding

```
        ┌─────────┐
        │ Router  │
        └────┬────┘
      ┌──────┼──────┐
      ▼      ▼      ▼
   Cache1  Cache2  Cache3
```

---

## Step 6 — Rate Limiting

### Goal

Protect system from overload.

---

### Token Bucket Model

```
Bucket (capacity = 5)

Tokens: ● ● ● ● ●

Each request = 1 token
```

---

### Diagram

```
Request → [Bucket] → allowed?
                ↓
           empty → reject
```

---

## Step 7 — Load Shedding

### Idea

Drop requests when overloaded.

---

### Flow

```
Incoming Requests
        │
        ▼
   System Capacity
        │
        ├── accept (within limit)
        └── reject (overflow)
```

---

### Visualization

```
Requests: 100
Capacity: 60

→ 60 processed
→ 40 dropped
```

---

## Step 8 — Batching & Pagination

---

### Batching

Combine multiple requests.

```
Instead of:
GET /user/1
GET /user/2

Do:
GET /users?ids=1,2
```

---

### Diagram

```
Clients → API → DB
   10 calls        1 call
```

---

### Pagination

Avoid large responses.

```
GET /products?page=1&limit=10
```

---

### Visualization

```
All data:
[1..1000]

Page 1:
[1..10]
```

---

# 🧠 6. Mental Model

---

## Components

```
[Client]
   ↓
[API]
   ↓
[Cache] ↔ [DB]
```

---

## Data Flow

```
READ:
Client → API → Cache → DB (if miss)

WRITE:
Client → API → DB → Cache
```

---

## Invariants

- Cache is best-effort
- DB is source of truth
- Cache must be invalidated

---

# 🏗️ 7. Final System Design

---

## System Diagram

```
           ┌──────────┐
           │  Client  │
           └────┬─────┘
                ▼
           ┌──────────┐
           │   API    │
           └────┬─────┘
                ▼
        ┌──────────────┐
        │ Rate Limiter │
        └────┬─────────┘
             ▼
        ┌──────────────┐
        │   Cache      │
        └────┬─────────┘
             ▼
        ┌──────────────┐
        │    DB        │
        └──────────────┘
```

---

## Request Flow

```
1. Check rate limit
2. Check cache
3. If miss → DB
4. Store in cache
5. Return response
```

---

# 🔧 8. Implementation Perspective

---

## Pseudo Flow

```
handleRequest(key):
    if not rateLimiter.allow():
        return 429

    value = cache.get(key)

    if value:
        return value

    value = db.get(key)

    cache.set(key, value, ttl=60)

    return value
```

---

# 🧪 9. Walkthrough Example

---

### Request: GET /product/123

```
Step 1: Rate limiter → OK
Step 2: Cache → MISS
Step 3: DB → fetch
Step 4: Cache → store
Step 5: Response → user
```

---

### Visual Trace

```
User
 ↓
API
 ↓
Cache (miss)
 ↓
DB (fetch)
 ↓
Cache (store)
 ↓
User (response)
```

---

# ⏱️ 10. Performance & Scalability

---

## Bottleneck Without Cache

```
All traffic → DB ❌
```

---

## With Cache

```
         ┌──── Cache (90%) ────┐
Traffic ─┤                     ├→ DB (10%)
         └─────────────────────┘
```

---

## Scaling Cache

```
        Router
          │
    ┌─────┼─────┐
    ▼     ▼     ▼
 Cache1 Cache2 Cache3
```

---

# ⚖️ 11. Tradeoffs and Alternatives

---

## Cache vs No Cache

```
No Cache:
User → API → DB

With Cache:
User → API → Cache → DB
```

---

## Tradeoffs

| Strategy        | Pros        | Cons           |
|----------------|------------|----------------|
| Cache-Aside    | flexible   | stale data     |
| Write-Through  | consistent | slower writes  |
| Write-Back     | fast       | data loss risk |

---

# ⚠️ 12. Common Mistakes

---

## 1. No Invalidation

```
Cache: old
DB: new
```

---

## 2. Cache Stampede

```
Cache expires
↓
1000 requests → DB ❌
```

---

## 3. No Rate Limiting

```
Traffic spike → system crash
```

---

# 🌍 13. Real-World Usage

- CDNs (Cloudflare)
- Redis caching
- API gateways
- Databases (buffer pools)

---

# 🚀 14. Variations and Extensions

---

## Multi-Level Cache

```
Client
 ↓
L1 (local cache)
 ↓
L2 (Redis)
 ↓
DB
```

---

## Write Queue (for write-back)

```
Cache → Queue → Worker → DB
```

---

# 🔁 15. Recap (Feynman Compression)

We:

- store frequently used data in cache
- avoid hitting DB every time
- control traffic with rate limiting
- drop excess load when needed
- batch and paginate to reduce work

👉 Result: fast, scalable system

---

# 🧩 16. Exercises

---

### Easy

1. Why does cache-aside reduce DB load?
2. What happens if TTL is too long?

---

### Intermediate

3. Design cache invalidation for user profile updates

---

### Real-World Challenge

4. Design a system for:
   - 10M users
   - heavy read traffic
   - hot keys

👉 Include:
- caching
- rate limiting
- load shedding