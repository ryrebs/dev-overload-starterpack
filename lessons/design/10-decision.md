# 🧠 System Design Decision Framework: When to Cache, Queue, Shard, Split & Trade Consistency

---

# 2. Who This Is For

- Intermediate → Senior engineers
- You’ve built APIs, used DBs, maybe touched distributed systems
- Want to **make better architecture decisions (not just know patterns)**

---

# 3. Problem Definition

### Real-world scenario

You’re building a system (e.g., marketplace, fintech app, social app):

You must decide:

- Should I add a cache?
- Do I need a queue?
- Should I shard my DB?
- Should I split services?

---

### Example

```
User → API → DB
```

System starts simple…

But then:

- traffic increases
- latency spikes
- DB struggles
- features grow

---

### Constraints

- 1k → 1M users
- latency < 100ms
- limited budget
- evolving product

---

### Core Problem

👉 **How do you choose the RIGHT tool at the RIGHT time?**

---

# 🧠 4. First Principles Thinking

---

## Why does this problem exist?

Because:

👉 Systems grow faster than their original design  
👉 Tradeoffs are unavoidable  
👉 Every optimization adds complexity

---

## What breaks without decisions?

```
Everything is synchronous
Everything hits DB
Everything tightly coupled
```

---

## Naive System

```
        ┌─────────┐
User →  │  API    │ → DB
        └─────────┘
```

---

## At Scale

```
Users ↑↑↑
   ↓
API overloaded
   ↓
DB overloaded ❌
```

---

## Why it fails

- No separation of concerns
- No load control
- No scaling strategy

---

# 🧭 5. Build the Intuition (Step-by-Step)

---

## Step 1 — Add Cache (When to Use Cache)

---

### Problem

Repeated reads overload DB

```
GET /product/1 repeated 1000x
```

---

### Add Cache

```
User → API → Cache → DB
```

---

### Diagram

```
        ┌─────────┐
User →  │  API    │
        └────┬────┘
             ▼
        ┌─────────┐
        │ Cache   │
        └────┬────┘
             ▼
             DB
```

---

### Use Cache WHEN:

✔ Read-heavy  
✔ Same data reused  
✔ Slight staleness acceptable  

---

### DON'T use cache WHEN:

```
Highly dynamic data
Strict consistency required
```

---

---

## Step 2 — Add Queue (When to Use Queue)

---

### Problem

Slow operations block user

```
API → Email → Payment → DB → Response ❌
```

---

### Add Queue

```
API → Queue → Worker
```

---

### Diagram

```
User → API → Queue → Worker
```

---

### Use Queue WHEN:

✔ Async tasks (email, logs, processing)  
✔ Decoupling services  
✔ Traffic spikes  

---

### DON'T use queue WHEN:

```
User needs immediate response
Strong consistency required
```

---

---

## Step 3 — Denormalization

---

### Problem

Joins are slow

```
User + Orders + Payments → JOIN
```

---

### Denormalize

Store combined data

---

### Diagram

```
Before:
User Table + Order Table

After:
UserWithOrders Table
```

---

### Visualization

```
Query:
User → Orders → Payments (slow ❌)

Denormalized:
Single read ✔
```

---

### Use WHEN:

✔ Read-heavy  
✔ Complex joins  
✔ Analytics  

---

### DON'T use WHEN:

```
Frequent updates
Strict consistency needed
```

---

---

## Step 4 — Sharding

---

### Problem

Single DB overloaded

```
All data → one DB ❌
```

---

### Shard

Split data across nodes

---

### Diagram

```
        Router
          │
   ┌──────┼──────┐
   ▼      ▼      ▼
 DB1     DB2     DB3
```

---

### Use WHEN:

✔ DB size too large  
✔ write throughput too high  

---

### DON'T use WHEN:

```
Small system
Complex queries across shards needed
```

---

---

## Step 5 — Split Services

---

### Problem

Monolith grows

```
API → everything
```

---

### Split

```
User Service
Order Service
Payment Service
```

---

### Diagram

```
       API Gateway
      ┌────┼────┐
      ▼    ▼    ▼
   User Order Payment
```

---

### Use WHEN:

✔ Teams scaling  
✔ Independent deployments needed  
✔ clear boundaries  

---

### DON'T use WHEN:

```
Small team
Early stage
High coordination overhead
```

---

---

## Step 6 — When NOT to Use Microservices

---

### Anti-pattern

```
Tiny services everywhere ❌
```

---

### Broken System

```
Service A → Service B → Service C → Service D
```

---

### Problems

- network latency
- debugging hell
- deployment complexity

---

### Visualization

```
1 request → 10 services → slow + fragile ❌
```

---

---

## Step 7 — Consistency Tradeoffs

---

### Strong Consistency

```
Write → immediately visible everywhere
```

---

### Eventual Consistency

```
Write → visible later
```

---

### Diagram

```
Time →
Write: ✔
Read:     ✔ (later)
```

---

### Choose Strong WHEN:

✔ financial systems  
✔ critical correctness  

---

### Choose Eventual WHEN:

✔ scalability needed  
✔ acceptable delay  

---

---

## Step 8 — Cost vs Performance Tradeoff

---

### Problem

More performance = more cost

---

### Diagram

```
Performance ↑
   ↑
Cost ↑
```

---

### Example

```
Cache → faster but costs memory
Sharding → faster but costs infra
```

---

### Visualization

```
Cheap system:
1 DB → slow

Expensive system:
Cache + Queue + Shards → fast
```

---

# 🧠 6. Mental Model

---

## Core Idea

👉 Every tool solves a bottleneck

---

## Mapping

```
Problem → Solution

Slow reads → Cache
Slow writes → Queue
Large DB → Sharding
Complex joins → Denormalization
Scaling teams → Service split
```

---

## System View

```
User
 ↓
API
 ↓
[Cache] → [Queue] → [Services]
 ↓
DB (sharded)
```

---

## Before vs After

---

### Before

```
User → API → DB
```

---

### After

```
User → API → Cache → Queue → Services → DB shards
```

---

# 🏗️ 7. Final System Design

---

## Full Architecture

```
           ┌──────────┐
           │  Client  │
           └────┬─────┘
                ▼
           ┌──────────┐
           │   API    │
           └────┬─────┘
      ┌─────────┼─────────┐
      ▼         ▼         ▼
   Cache      Queue     Services
                  │        │
                  ▼        ▼
               Workers   DB Shards
```

---

## Request Flow

```
1. Read → Cache
2. Write → Queue
3. Process → Worker
4. Store → DB shard
```

---

## Data Flow

```
User → API → Cache/Queue → Services → DB
```

---

# 🔧 8. Implementation Perspective

---

## Typical Stack

- Cache: Redis
- Queue: Kafka / SQS
- DB: Postgres / DynamoDB
- Services: microservices (carefully!)

---

## Pseudo Flow

```
read():
    if cache:
        return cache
    return db

write():
    queue.send(job)
```

---

# 🧪 9. Walkthrough Example

---

### User places order

---

### Flow

```
1. API receives request
2. Writes to queue
3. Worker processes payment
4. DB updated
5. Cache invalidated
```

---

### Visual Trace

```
User
 ↓
API
 ↓
Queue
 ↓
Worker
 ↓
DB
 ↓
Cache updated
```

---

# ⏱️ 10. Performance & Scalability

---

## Bottleneck

```
All traffic → DB ❌
```

---

## Scaled System

```
         ┌──── Cache ────┐
Traffic ─┤               ├→ DB shards
         └──── Queue ────┘
```

---

## Horizontal Scaling

```
Queue
 ├ Worker1
 ├ Worker2
 ├ Worker3
```

---

# ⚖️ 11. Tradeoffs and Alternatives

---

## Cache vs No Cache

```
No cache:
User → DB

With cache:
User → Cache → DB
```

---

## Queue vs Sync

```
Sync:
API → DB

Async:
API → Queue → Worker → DB
```

---

## Microservices vs Monolith

```
Monolith:
Simple, fast dev

Microservices:
Scalable, complex
```

---

# ⚠️ 12. Common Mistakes

---

## 1. Premature Optimization

```
Adding cache/queue too early ❌
```

---

## 2. Over-sharding

```
Too many DBs → complexity ❌
```

---

## 3. Microservice explosion

```
Too many services ❌
```

---

## Broken System

```
User → API → 10 services → DB
         ↓
     slow + fragile ❌
```

---

# 🌍 13. Real-World Usage

- Netflix (event-driven + microservices)
- Amazon (queues + async processing)
- Facebook (heavy caching)
- Uber (sharded DB + event systems)

---

# 🚀 14. Variations and Extensions

---

## Hybrid Architecture

```
Critical path → sync
Non-critical → async
```

---

### Diagram

```
API
 ├ sync → DB
 └ async → Queue
```

---

## Multi-Level Scaling

```
Cache (L1)
Queue
DB shards
```

---

# 🔁 15. Recap (Feynman Compression)

👉 Systems break because of:

- too many reads
- slow operations
- large data
- tight coupling

👉 We fix by:

- cache → reduce reads
- queue → async work
- denormalize → faster reads
- shard → scale DB
- split services → scale teams

---

# 🧩 16. Exercises

---

### Easy

1. When should you NOT use a cache?
2. Why is queue useful for async work?

---

### Intermediate

3. Design system with:
   - read-heavy traffic
   - moderate writes
   - low latency

---

### Real-World Challenge

4. Design system for:

- 10M users
- heavy reads
- async processing
- limited budget

👉 Decide:
- cache?
- queue?
- sharding?
- service split?