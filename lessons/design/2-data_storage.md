# Data Systems from First Principles: Modeling, Scaling, and Consistency

---

## 1. Title

**Designing Data Systems from First Principles: From Tables to Planet-Scale Storage**

---

## 2. Who This Is For

- Intermediate engineers
- Backend / full-stack developers
- System design interview candidates

**Required background:**
- APIs
- basic databases (CRUD)
- simple SQL

---

## 3. Problem Definition

---

### Real-world problem

We need to design a system that:

- stores user data
- supports reads/writes at scale
- maintains correctness
- scales to millions of users

---

### Example

Design a **social media backend**:

- users
- posts
- comments

---

### Constraints

| Constraint | Example |
|----------|--------|
| Users | 50M |
| Writes | 10K/sec |
| Reads | 100K/sec |
| Latency | <100ms |
| Consistency | eventual OK for feeds |
| Storage | TB–PB scale |

---

## 🧠 4. First Principles Thinking

---

### Why does this problem exist?

Because data must be:

- stored
- queried
- consistent
- scalable

---

### Naive solution

```
User → Server → Single DB
```

---

### Diagram

```
[User]
   ↓
[API]
   ↓
[Single Database]
```

---

### What breaks?

```
Too many users
     ↓
DB overloaded
     ↓
Slow queries / downtime
```

---

## 🧭 5. Build the Intuition (Step-by-Step)

---

### Step 1 — Data Modeling (structure first)

---

#### Example tables

```
Users
+----+------+
| id | name |
+----+------+

Posts
+----+--------+---------+
| id | userID | content |
+----+--------+---------+
```

---

#### Relationship

```
User (1) ────── (many) Posts
```

---

### Step 2 — SQL vs NoSQL

---

#### SQL (structured)

```
[Users Table] ← join → [Posts Table]
```

Pros:
- strong consistency
- joins

---

#### NoSQL (denormalized)

```
User Document:
{
  id,
  posts: [...]
}
```

Pros:
- fast reads
- flexible schema

---

### Decision flow

```
Need joins + consistency?
   → SQL

Need scale + flexible?
   → NoSQL
```

---

### Step 3 — Indexing (speed up reads)

---

#### Without index

```
Scan entire table
[1][2][3][4][5][6] → find user_id=5
```

---

#### With index

```
Index:
user_id → row pointer

Find directly → O(log n)
```

---

### Diagram

```
[Table]
   ↓
[Index Layer]
   ↓
Fast lookup
```

---

### Step 4 — Transactions & Isolation

---

#### Problem

```
Two users update same data
```

---

#### Without transaction

```
Write A
Write B
→ inconsistent
```

---

#### With transaction

```
BEGIN
  write A
  write B
COMMIT
```

---

#### Isolation levels (conceptual)

```
Weak → faster → dirty reads
Strong → slower → consistent
```

---

### Step 5 — Replication (scale reads)

---

#### Before

```
[DB]
 ↑ ↑ ↑
all reads + writes
```

---

#### After

```
        [Replica]
       /
[Primary DB]
       \
        [Replica]
```

---

### Flow

```
Writes → Primary
Reads → Replicas
```

---

### Step 6 — Partitioning / Sharding

---

#### Problem

```
Single DB too big
```

---

#### Solution

```
Shard by user_id

Shard 1 → users 1–1M
Shard 2 → users 1M–2M
Shard 3 → ...
```

---

### Diagram

```
          [Router]
         /   |   \
      DB1  DB2  DB3
```

---

### Step 7 — Denormalization

---

#### Problem

Joins are slow at scale.

---

#### Solution

Duplicate data:

```
Post:
{
  id,
  user_name,   ← duplicated
  content
}
```

---

#### Tradeoff

```
Faster reads
But harder updates
```

---

### Step 8 — Data Lifecycle

---

#### Problem

Data grows forever.

---

#### Solution

```
Hot data → fast DB
Warm data → cheaper storage
Cold data → archive
```

---

### Diagram

```
Recent → DB
Older → Storage
Oldest → Archive
```

---

## 🧠 6. Mental Model

---

### Full data system flow

```
User
 ↓
API
 ↓
Cache (optional)
 ↓
Primary DB
 ↓
Replicas
 ↓
Shards
 ↓
Archive
```

---

### Invariants

- data must be retrievable
- writes must not corrupt state
- reads must be fast enough
- system must scale

---

## 🏗️ 7. Final System Design

---

### Architecture

```
Users
  ↓
API Layer
  ↓
Cache
  ↓
Router
  ↓
Shard Cluster
   ├── Primary
   ├── Replica
   └── Replica
  ↓
Archive Storage
```

---

### Request Flow

```
Read:
User → API → Cache → DB Replica

Write:
User → API → Primary DB → Replicate
```

---

## 🔧 8. Implementation Perspective

---

### Real-world mapping

| Component | Example |
|----------|--------|
| SQL DB | PostgreSQL |
| NoSQL | MongoDB |
| Cache | Redis |
| Sharding | custom / Vitess |
| Replication | built-in DB |

---

### Write flow

```
API:
BEGIN
write to DB
COMMIT
replicate async
```

---

## 🧪 9. Walkthrough Example

---

### Request: fetch user posts

```
1. User requests feed
2. API checks cache
3. Cache miss
4. API queries DB replica
5. DB returns posts
6. Cache stores result
7. Response returned
```

---

### Visual trace

```
User
 ↓
API
 ↓
Cache (miss)
 ↓
Replica DB
 ↓
Response
```

---

## ⏱️ 10. Performance & Scalability

---

### Bottleneck

```
All traffic → single DB
```

---

### Diagram

```
Too many queries
      ↓
DB overloaded
      ↓
Latency spikes
```

---

### Scaled system

```
Add:
- replicas
- shards
- cache
```

---

### Diagram

```
Users
 ↓
Cache
 ↓
Shard cluster
```

---

## ⚖️ 11. Tradeoffs and Alternatives

---

### SQL vs NoSQL

```
SQL:
+ consistency
- harder to scale

NoSQL:
+ scale
- weaker consistency
```

---

### Normalization vs Denormalization

```
Normalized:
+ clean data
- slow joins

Denormalized:
+ fast reads
- duplication
```

---

## ⚠️ 12. Common Mistakes

---

### ❌ No index

```
Query → full scan → slow
```

---

### ❌ No sharding

```
DB grows → cannot scale
```

---

### ❌ Strong consistency everywhere

```
Too slow system
```

---

### Broken diagram

```
Single DB
   ↓
Massive traffic
   ↓
System collapse
```

---

## 🌍 13. Real-World Usage

---

- :contentReference[oaicite:0]{index=0} → heavy denormalization + sharding  
- :contentReference[oaicite:1]{index=1} → fan-out + caching  
- :contentReference[oaicite:2]{index=2} → replication + partitioning  

---

## 🚀 14. Variations and Extensions

---

### Multi-region replication

```
Region A ↔ Region B
```

---

### Event sourcing

```
Write events → rebuild state
```

---

### CQRS

```
Write DB ≠ Read DB
```

---

## 🔁 15. Recap (Feynman Compression)

A data system:

- models data (tables / documents)
- speeds reads (index, cache)
- ensures correctness (transactions)
- scales reads (replication)
- scales writes (sharding)
- manages size (lifecycle)

---

## 🧩 16. Exercises

---

### Easy

1. Design tables for users + posts  
2. Add an index to speed lookup  

---

### Intermediate

3. Decide SQL vs NoSQL for a chat system  

---

### Real-world challenge

4. Design a scalable feed system:
   - 100M users
   - heavy reads
   - low latency

---

## 🧠 FINAL INSIGHT

All data systems are tradeoffs between:

```
Consistency
Speed
Scale
Cost
```

You cannot maximize all at once.