# System Design Core Decision-Making — Visual Modules

This is a **multi-module tutorial set**.  
Each module is independent, visual-first, and designed like a whiteboard walkthrough.

---

# Module 1 — Requirements Clarification

## 1. Title

**Requirements Clarification: Turning a Vague Request into a Buildable System**

## 2. Who This Is For

- Beginner to intermediate engineers
- Anyone doing system design interviews
- Anyone who jumps too quickly into architecture

**Background needed**
- APIs
- databases
- basic distributed systems vocabulary

## 3. Problem Definition

Real-world prompt:

> “Design a notification system.”

That could mean:

- push only
- push + email + SMS
- transactional only
- marketing campaigns
- 100 QPS or 1M QPS
- strong delivery guarantees or best-effort

### Concrete example

```
Request:
"Design a notification system for an e-commerce platform."
```

Possible hidden requirements:

- order shipped notification
- payment failed notification
- promo notifications
- user preference controls
- deduplication
- retry on provider failure

### Constraints

| Dimension | Example |
|---|---|
| Scale | 50M users |
| Peak sends | 500K/min |
| Latency | transactional < 5s |
| Reliability | retries required |
| Cost | SMS expensive |
| Compliance | opt-out, region rules |

## 4. First Principles Thinking

### Why does this problem exist?

Because product asks for a “system,” but systems are built from **requirements**, not buzzwords.

### What breaks without clarification?

- overbuilt system
- underbuilt system
- wrong database
- wrong consistency model
- wrong SLA
- wrong cost profile

### Naive approach

```
PM request
   ↓
Engineer starts drawing:
Load Balancer → API → DB → Queue → Workers
```

### Why this fails

Because architecture before requirements creates the wrong shape.

### Naive flow diagram

```
[Vague prompt]
     ↓
[Pick random architecture]
     ↓
[Implement]
     ↓
[Discover missing requirements]
     ↓
[Rewrite system]
```

## 5. Build the Intuition (Step-by-Step)

### Step 1 — Separate functional vs non-functional

```
                [System Request]
                 /            \
                /              \
     [Functional]            [Non-Functional]
   "What it does"         "How well it must do it"
```

Functional examples:
- send notification
- schedule notification
- retry failed delivery

Non-functional examples:
- p99 latency
- availability
- durability
- throughput
- cost

### Step 2 — Find the primary path

Ask:

```
What is the one request that must absolutely work?
```

Example:

```
Order shipped
   ↓
Must notify user within 5 seconds
```

### Step 3 — Split must-have vs nice-to-have

```
Must-have:
- send push/email
- retry
- user preferences

Nice-to-have:
- A/B testing
- analytics dashboards
- campaign builder
```

### Step 4 — Find the real bottleneck question

```
Is this mostly about:
- latency?
- throughput?
- reliability?
- cost?
- consistency?
```

## 6. Mental Model

### Requirements tree

```
                 [Design X]
                     |
      ----------------------------------
      |                |               |
 [Users]          [Traffic]       [Correctness]
      |                |               |
  who uses it?    how much?      what can go wrong?
```

### Invariants to identify

- can duplicate sends happen?
- can data be stale?
- can requests be retried safely?
- what is the SLO?

## 7. Final System Design View for This Module

### Requirements clarification board

```
[Prompt]
   ↓
[Functional requirements]
   ↓
[Non-functional requirements]
   ↓
[Out of scope]
   ↓
[Capacity assumptions]
   ↓
[Prioritized architecture decisions]
```

### Responsibilities

| Step | Purpose |
|---|---|
| Functional clarification | defines behavior |
| Non-functional clarification | defines constraints |
| Scope control | prevents architecture explosion |
| Prioritization | tells you what to optimize |

## 8. Implementation Perspective

### Real engineer flow

```
1. Restate prompt
2. Clarify users + use cases
3. Clarify scale
4. Clarify latency/reliability
5. Define assumptions
6. Start architecture
```

### Sequence

```
Interviewer/PM → Engineer: "Design notifications"
Engineer → PM: "Transactional only, or marketing too?"
Engineer → PM: "Peak sends?"
Engineer → PM: "Delivery guarantee?"
Engineer → Engineer: "Now architecture makes sense"
```

## 9. Walkthrough Example

### Example clarification trace

```
Prompt: Design notifications

Q1: Which channels?
A1: Push + email first

Q2: Are all notifications equal?
A2: No. Transactional is highest priority

Q3: Delivery guarantee?
A3: At-least-once is acceptable

Q4: Peak?
A4: 500K/min during campaigns
```

### Resulting architecture direction

```
Because:
- at-least-once
- high throughput
- async okay

We likely want:
API → Queue → Workers → Providers
```

## 10. Performance & Scalability

### Bottleneck if you skip clarification

```
Wrong requirement assumption
        ↓
Wrong architecture
        ↓
Wrong bottleneck optimization
        ↓
System misses target
```

## 11. Tradeoffs and Alternatives

### Compare

```
Without clarification:
Prompt → Architecture

With clarification:
Prompt → Questions → Constraints → Architecture
```

## 12. Common Mistakes

### Broken system diagram

```
[Product need: low latency transactional]
                 ↓
[Engineer designs batch system]
                 ↓
[Users get delayed notifications]
```

Other mistakes:
- treating all traffic equally
- not defining success metrics
- not defining failure behavior
- no scope boundaries

## 13. Real-World Usage

This appears in every serious design review:
- API platforms
- payments
- notifications
- feed systems
- internal infrastructure

## 14. Variations and Extensions

### B2C product system

```
More user variability
More traffic spikes
More cost sensitivity
```

### Internal enterprise system

```
Fewer users
More compliance
More correctness requirements
```

## 15. Recap (Feynman Compression)

Requirements clarification means:

- define what the system does
- define what matters most
- define scale and failure tolerance
- only then design architecture

## 16. Exercises

1. Clarify requirements for a URL shortener.
2. Clarify requirements for a metrics ingestion system.
3. Intermediate: Clarify requirements for a ride-matching service.
4. Real-world: Take “design chat system” and produce a full functional/non-functional requirements board.

---

# Module 2 — Capacity Estimation

## 1. Title

**Capacity Estimation: Rough Math That Prevents Bad Architecture**

## 2. Who This Is For

- Engineers who know components but not sizing
- Interview candidates
- Backend engineers making scaling decisions

**Background needed**
- QPS
- storage basics
- bandwidth basics

## 3. Problem Definition

We need to estimate:

- traffic
- read/write mix
- storage
- memory
- network
- growth

### Example

Design an image metadata API.

Assumptions:
- 20M daily active users
- 5 requests/user/day
- 100B metadata record
- 3 replicas

## 4. First Principles Thinking

### Why does this problem exist?

Because component choice depends on size.

### What breaks without it?

- DB too small
- cache too small
- wrong partition count
- underestimated cost

### Naive approach

```
"Let's use PostgreSQL + Redis + Kafka."
```

No numbers.

### Why this fails

Because architecture without load estimates is guesswork.

### Naive flow

```
[Choose tech]
    ↓
[Traffic grows]
    ↓
[Unexpected bottleneck]
    ↓
[Emergency scaling]
```

## 5. Build the Intuition (Step-by-Step)

### Step 1 — Estimate requests

```
20M users/day
× 5 req/user/day
= 100M req/day

100M / 86400 (sec) ≈ 1157 req/s average
Peak ≈ 5x average
Peak ≈ 6K req/s
```

### Step 2 — Split reads and writes

```
Total peak = 6K QPS (Queries per second)

Assume:
Reads 90% = 5.4K QPS
Writes 10% = 600 QPS
```

### Step 3 — Estimate storage

```
100M writes/day
× 100 bytes (Assume 100 bytes as size per record)
= 10 GB/day raw

With indexes + metadata ~ 3x
= 30 GB/day

With 30 days retention:
≈ 900 GB

With replication factor 3:
≈ 2.7 TB
```

### Step 4 — Estimate bandwidth

```
6K req/s
× 2 KB/response (Rough estimate of average response size)
= 12 MB/s * 8 bits
≈ 96 Mbps
```

## 6. Mental Model

### Estimation flow

```
Users
  ↓
Requests
  ↓
Read/write split
  ↓
Data size
  ↓
Storage
  ↓
Network / memory / partitions
```

### Invariant

Rough math does not need to be perfect.  
It needs to be **directionally correct**.

## 7. Final System Design View for This Module

### Capacity board

```
Users/day
   ↓
Peak QPS
   ↓
Read/write ratio
   ↓
Storage/day
   ↓
Retention
   ↓
Replication
   ↓
Infra sizing
```

## 8. Implementation Perspective

### What engineers actually do

- estimate peak load, not just average
- add safety margin
- size for replication
- size for indexes and metadata
- revisit monthly

### Pseudo-flow

```
product forecast
   ↓
traffic estimate
   ↓
infra estimate
   ↓
cost estimate
   ↓
architecture review
```

## 9. Walkthrough Example

### Example request

```
30M users
3 uploads/day
1 KB metadata/write
peak factor 4
```

Compute:

```
Writes/day = 90M
Average write QPS ≈ 1041
Peak write QPS ≈ 4.2K
```

Storage:

```
90M × 1 KB = 90 GB/day raw
With replication x3 = 270 GB/day
```

## 10. Performance & Scalability

### Bottleneck diagram

```
Underestimated QPS
      ↓
Too few servers
      ↓
CPU saturation
      ↓
Latency spike
```

### Scaled system diagram

```
[Traffic estimate]
      ↓
[Autoscaling threshold]
      ↓
[Enough stateless nodes]
      ↓
[Stable latency]
```

## 11. Tradeoffs and Alternatives

### Overestimate vs underestimate

```
Overestimate:
higher cost
lower risk

Underestimate:
lower cost
higher outage risk
```

## 12. Common Mistakes

### Broken diagram

```
Use average QPS only
      ↓
Ignore peak
      ↓
Traffic spike
      ↓
Queue overflow / API timeout
```

Other mistakes:
- forgetting replicas
- forgetting retention
- ignoring index overhead
- ignoring batch jobs

## 13. Real-World Usage

Used in:
- database sizing
- Kafka partition planning
- cache sizing
- CDN bandwidth planning
- shard count estimation

## 14. Variations and Extensions

### Burst-heavy system

```
Average low
Peak very high
→ queue and backpressure matter more
```

### Write-heavy system

```
More WAL / replication / partitioning pressure
```

## 15. Recap (Feynman Compression)

Capacity estimation is rough math to translate product scale into system size.

## 16. Exercises

1. Estimate QPS for a feed read service.
2. Estimate storage for a logging system.
3. Intermediate: estimate partitions for an event stream.
4. Real-world: size a photo metadata service for 100M DAU.

---

# Module 3 — Latency vs Throughput

## 1. Title

**Latency vs Throughput: Optimizing the Right Performance Goal**

## 2. Who This Is For

- Engineers optimizing APIs or pipelines
- Interview candidates
- Backend and infrastructure engineers

**Background needed**
- request-response model
- queues
- parallelism basics

## 3. Problem Definition

We must decide whether to optimize for:

- **latency** = how fast one request finishes
- **throughput** = how many requests total the system handles

### Example

Two systems:

- payments API → latency-sensitive
- analytics ingestion pipeline → throughput-sensitive

## 4. First Principles Thinking

### Why does this problem exist?

Because fast per-request response and high total volume are related, but not identical.

### Naive approach

```
"Make it fast."
```

### Why it fails

Because “fast” could mean:

- one request returns in 20ms
- or system handles 1M events/sec

Not the same target.

### Naive flow

```
One optimization goal assumed
          ↓
Wrong queue / batching / replication choices
          ↓
System misses business goal
```

## 5. Build the Intuition (Step-by-Step)

### Step 1 — Define the two metrics

```
Latency:
request start → request end

Throughput:
completed requests per second
```

### Step 2 — See the tension

```
More batching
   ↓
Higher throughput
   ↓
Often higher latency
```

### Step 3 — Visual comparison

Low-latency API:

```
User → API → DB → Response
```

High-throughput pipeline:

```
Producers → Queue → Batch Workers → Storage
```

### Step 4 — Pick by business need

```
Checkout page?
→ latency wins

Event analytics?
→ throughput wins
```

## 6. Mental Model

### Comparison diagram

```
Latency path:
[one request] ─────────────────────────→ done

Throughput view:
[req][req][req][req][req] → total completed / second
```

### Invariant

Optimizations should match primary business value.

## 7. Final System Design View for This Module

### Latency-optimized design

```
Client
  ↓
LB
  ↓
Fast API
  ↓
Cache
  ↓
DB
```

### Throughput-optimized design

```
Producers
  ↓
Queue
  ↓
Batch workers
  ↓
Storage
```

## 8. Implementation Perspective

### Latency tools

- caching
- fewer network hops
- precomputation
- local replicas

### Throughput tools

- batching
- queueing
- async workers
- partitioning

## 9. Walkthrough Example

### Same feature, two designs

#### Notification send

Latency-first:
```
User action → immediate push
```

Throughput-first:
```
Campaign → queue → batch send
```

## 10. Performance & Scalability

### Bottleneck diagrams

Latency bottleneck:
```
Too many hops
Client → Gateway → Service A → Service B → DB
```

Throughput bottleneck:
```
Too little batching
Many tiny writes → DB pressure
```

### Scaled versions

Latency scaled:
```
Cache + read replica + colocated services
```

Throughput scaled:
```
Queue + more consumers + partitioned storage
```

## 11. Tradeoffs and Alternatives

```
Lower latency:
less batching
more cost

Higher throughput:
more batching
more waiting
```

## 12. Common Mistakes

### Broken system diagram

```
User-facing API
    ↓
Huge queue
    ↓
Batch worker
    ↓
Response after seconds
```

Wrong because user request needed low latency.

## 13. Real-World Usage

- search autocomplete → latency
- payment auth → latency
- log ingestion → throughput
- analytics ETL → throughput

## 14. Variations and Extensions

### Hybrid architecture

```
Fast path:
transactional requests

Slow path:
async analytics / side effects
```

## 15. Recap (Feynman Compression)

Latency is how fast one request finishes.  
Throughput is how much total work the system can process.

## 16. Exercises

1. Classify a chat send API as latency or throughput sensitive.
2. Classify a nightly analytics job.
3. Intermediate: redesign a system to improve throughput without hurting p95 too much.
4. Real-world: split an e-commerce checkout into latency-critical and throughput-oriented paths.

---

# Module 4 — Consistency vs Availability (CAP Tradeoffs)

## 1. Title

**Consistency vs Availability: Choosing Behavior During Network Partitions**

## 2. Who This Is For

- Engineers working with distributed data
- System design interview candidates
- Backend engineers designing replicated systems

**Background needed**
- replication basics
- leader/follower basics
- failure basics

## 3. Problem Definition

When systems are distributed, network partitions happen.

Then you often must choose:

- **Consistency**: all clients see the latest agreed value
- **Availability**: system continues serving responses

### Example

Bank balance vs social media likes.

## 4. First Principles Thinking

### Why does this problem exist?

Because copies of data live on multiple machines, and machines can’t always talk.

### Naive assumption

```
Replicate everywhere
and get:
- perfect consistency
- perfect availability
- no failures
```

Impossible under partition.

### Naive diagram

```
Client A → DC1
Client B → DC2

DC1 X----network partition----X DC2
```

Naive expectation:
```
Both sides stay writable and perfectly synchronized
```

## 5. Build the Intuition (Step-by-Step)

### Step 1 — Single node is easy

```
Client → DB
```

No replica disagreement.

### Step 2 — Add replication

```
Client → Replica A
Client → Replica B
```

Now disagreement is possible.

### Step 3 — Add partition

```
Replica A   X   Replica B
```

Question:

```
If writes arrive on both sides, what should happen?
```

### Step 4 — CP choice

```
Partition happens
    ↓
Reject some operations
    ↓
Preserve correctness
```

### Step 5 — AP choice

```
Partition happens
    ↓
Keep serving
    ↓
Reconcile later
```

## 6. Mental Model

### CAP diagram

```
                 [Partition]
                      |
          ---------------------------
          |                         |
   [Choose Consistency]      [Choose Availability]
          |                         |
   reject or block writes      accept divergent writes
```

### Invariant examples

CP invariant:
```
No conflicting visible state
```

AP invariant:
```
Service continues operating
```

## 7. Final System Design View for This Module

### CP-oriented example

```
Clients
  ↓
Leader
  ↓
Quorum replicas
```

If quorum unavailable:
```
write fails
```

### AP-oriented example

```
Clients → local region replica
          local writes accepted
          reconciliation later
```

## 8. Implementation Perspective

### CP systems often use

- quorum writes (A write is considered successful once a majority of replicas confirm it.)
- leader election
- consensus

### AP systems often use

- conflict resolution
- version vectors
- eventual consistency

## 9. Walkthrough Example

### Example: inventory count

Partition:

```
Region A thinks stock = 1
Region B thinks stock = 1
```

CP approach:
```
One side blocks write
```

AP approach:
```
Both sides may sell
Reconcile later
```

## 10. Performance & Scalability

### Bottleneck / behavior diagram

CP:
```
Partition → write rejection → lower availability
```

AP:
```
Partition → stale/conflicting data → reconciliation work
```

## 11. Tradeoffs and Alternatives

### Comparison

```
CP:
better correctness
worse availability during partitions

AP:
better availability
weaker freshness / correctness
```

## 12. Common Mistakes

### Broken system diagram

```
Multi-region active-active writes
          ↓
No conflict handling
          ↓
Data corruption
```

## 13. Real-World Usage

- payments and ledgers lean CP
- carts and feeds often tolerate AP
- DNS is highly availability-oriented
- inventory often uses hybrid patterns

## 14. Variations and Extensions

### Hybrid model

```
critical path = CP
non-critical path = AP
```

Example:
- payment charge → CP
- analytics counter → AP

## 15. Recap (Feynman Compression)

Under network partitions, distributed systems often trade between strict correctness and always responding.

## 16. Exercises

1. Pick CP or AP for a chat presence system.
2. Pick CP or AP for a payment ledger.
3. Intermediate: design a shopping cart with eventual consistency.
4. Real-world: split a ride-sharing system into CP and AP subsystems.

---

# Module 5 — Scalability (Vertical vs Horizontal)

## 1. Title

**Scalability: Vertical vs Horizontal Growth**

## 2. Who This Is For

- Backend engineers
- Platform engineers
- System design learners

**Background needed**
- servers
- load balancers
- state basics

## 3. Problem Definition

Your service grows from:

```
100 req/s → 100K req/s
```

How do you grow the system?

## 4. First Principles Thinking

### Naive approach

```
Buy bigger server
```

### Why this fails

- hardware ceiling
- expensive
- single point of failure

### Naive diagram

```
Users → BIGGER server → DB
```

## 5. Build the Intuition (Step-by-Step)

### Step 1 — Vertical scaling

```
same node
more CPU / RAM
```

Good for:
- simplicity
- early stage

### Step 2 — Horizontal scaling

```
Users
  ↓
LB
  ↓
S1 S2 S3 S4
```

Good for:
- elasticity
- fault tolerance

### Step 3 — Requirement for horizontal scaling

```
stateless app layer
```

## 6. Mental Model

### Comparison diagram

```
Vertical:
     [Bigger Box]

Horizontal:
 [Box][Box][Box][Box]
```

## 7. Final System Design View for This Module

### Preferred scalable pattern

```
Users
  ↓
Load Balancer
  ↓
Stateless Service Pool
  ↓
Cache / DB / Queue
```

## 8. Implementation Perspective

Vertical:
- increase instance size
- easy but limited

Horizontal:
- autoscaling
- service discovery
- health checks
- load balancing

## 9. Walkthrough Example

Traffic doubles.

Vertical path:
```
Resize instance
```

Horizontal path:
```
Add 4 more pods
```

## 10. Performance & Scalability

### Bottleneck diagram

```
Single giant server fails
      ↓
total outage
```

### Scaled diagram

```
10 servers
1 fails
9 remain
```

## 11. Tradeoffs and Alternatives

| Strategy | Pros | Cons |
|---|---|---|
| Vertical | simple | ceiling, risky |
| Horizontal | resilient | more operational complexity |

## 12. Common Mistakes

### Broken system

```
State stored in app memory
        ↓
Cannot safely scale out
```

## 13. Real-World Usage

- stateless APIs → horizontal
- some databases → mix of vertical + sharding
- caches → clustered horizontal scaling

## 14. Variations and Extensions

### Hybrid

```
Moderate vertical scaling first
Then horizontal scaling
```

## 15. Recap (Feynman Compression)

Vertical scaling means bigger machines.  
Horizontal scaling means more machines.

## 16. Exercises

1. When is vertical scaling enough?
2. Why do stateless services scale out better?
3. Intermediate: redesign a monolith for horizontal growth.
4. Real-world: scale an API from 1K QPS to 100K QPS.

---

# Module 6 — Stateless vs Stateful Design

## 1. Title

**Stateless vs Stateful Design: Where Should System Memory Live?**

## 2. Who This Is For

- API/backend engineers
- infra/platform learners
- interview candidates

**Background needed**
- sessions
- databases
- caches
- load balancers

## 3. Problem Definition

Should your service instance remember user-specific state locally?

### Example

Login session:
- store in server memory?
- or Redis / DB / token?

## 4. First Principles Thinking

### Naive design

```
User → Server 1
Server 1 memory stores session
```

### Why this fails

- server restart loses state
- load balancer may route next request elsewhere
- scaling becomes sticky and fragile

### Naive diagram

```
User → LB → Server 1(session in RAM)
             Server 2(no session)
```

## 5. Build the Intuition (Step-by-Step)

### Step 1 — Stateful app

```
Request depends on a specific server
```

### Step 2 — Sticky sessions

```
LB forces same user → same server
```

Improvement, but still brittle.

### Step 3 — Externalize state

```
User → API → Redis/DB/session store
```

Now any server can serve request.

## 6. Mental Model

### Before / after

Stateful:
```
User → specific server → local memory
```

Stateless:
```
User → any server → external state store
```

### Invariant

App layer should not be a single keeper of critical session state.

## 7. Final System Design View for This Module

```
Users
  ↓
LB
  ↓
Stateless API nodes
  ↓
Session store / DB / cache
```

## 8. Implementation Perspective

Stateless patterns:
- JWT
- Redis session store
- DB-backed session
- request carries enough context

## 9. Walkthrough Example

Login flow:

```
1. User logs in
2. Auth service creates token/session
3. Session stored externally or encoded in token
4. Any API instance can validate
```

## 10. Performance & Scalability

### Broken bottleneck

```
App memory session
      ↓
No smooth failover
      ↓
No safe autoscaling
```

## 11. Tradeoffs and Alternatives

Stateful can be okay for:
- DB nodes
- stream processors
- websocket session managers (with special handling)

Stateless is preferred for:
- API frontends
- request handlers

## 12. Common Mistakes

### Broken system diagram

```
Autoscaling adds servers
        ↓
Users lose sessions after rebalance
```

## 13. Real-World Usage

- frontend APIs are usually stateless
- databases are stateful
- Kafka brokers are stateful
- cache nodes are stateful

## 14. Variations and Extensions

### Hybrid architecture

```
Stateless control plane
Stateful data plane
```

## 15. Recap (Feynman Compression)

Stateless means any server can handle the request because important state is stored outside the server.

## 16. Exercises

1. Why do JWTs help stateless APIs?
2. Why are databases stateful?
3. Intermediate: redesign sticky-session auth into stateless auth.
4. Real-world: design websocket state distribution across nodes.

---

# Module 7 — Idempotency

## 1. Title

**Idempotency: Making Retries Safe**

## 2. Who This Is For

- API engineers
- payments/backend engineers
- system designers

**Background needed**
- HTTP basics
- retries
- request IDs
- DB writes

## 3. Problem Definition

Distributed systems retry requests.

Question:

```
If the same request arrives twice, will it produce the same effect?
```

### Example

Create payment.

If retried:
- charge once?
- or twice?

## 4. First Principles Thinking

### Why does this problem exist?

Because network failures make clients unsure whether a request succeeded.

### Naive approach

```
Client sends POST /charge
timeout happens
client retries
server charges again
```

### Naive diagram

```
Client → Charge API → Payment processor
   ↑ timeout
Client retries same request
   ↓
Charge API charges again
```

## 5. Build the Intuition (Step-by-Step)

### Step 1 — Recognize retry ambiguity

```
Timeout ≠ failure
Timeout may mean:
- request failed
- response lost
- request succeeded but client didn't know
```

### Step 2 — Add idempotency key

```
Request:
Idempotency-Key: abc123
```

### Step 3 — Store request result

```
If key new:
process + save result

If key seen:
return saved result
```

## 6. Mental Model

### Idempotency box

```
Client request
   ↓
[Idempotency check]
   ├── seen before → return old result
   └── new request → process and store result
```

### Invariant

Same idempotency key + same logical operation  
→ same visible result

## 7. Final System Design View for This Module

```
Client
  ↓
API
  ↓
Idempotency Store
  ↓
Business Logic
  ↓
DB / external provider
```

## 8. Implementation Perspective

Common implementation:
- idempotency key table in DB/Redis
- unique constraint
- store final response payload/status
- TTL if appropriate

## 9. Walkthrough Example

Payment:

```
1. Client sends charge with key K1
2. API checks store: not found
3. API creates charge
4. API stores result under K1
5. Response lost
6. Client retries with K1
7. API returns stored result
```

## 10. Performance & Scalability

### Bottleneck diagram

```
All retries hit full business logic
       ↓
duplicate side effects
```

### Safe diagram

```
Retries hit idempotency layer first
       ↓
duplicates short-circuit
```

## 11. Tradeoffs and Alternatives

- DB unique constraints can help
- full idempotency layer is stronger
- not every endpoint needs same level

## 12. Common Mistakes

### Broken system

```
Retry support added
      ↓
No idempotency key
      ↓
Duplicate orders / payments / emails
```

## 13. Real-World Usage

- Stripe-like payment APIs
- order creation
- job scheduling
- webhook receivers

## 14. Variations and Extensions

### Receiver-side idempotency

```
Webhook sender retries
Webhook receiver deduplicates
```

## 15. Recap (Feynman Compression)

Idempotency means retries do not create duplicate effects.

## 16. Exercises

1. Why do payments need idempotency?
2. Add idempotency to order creation.
3. Intermediate: design webhook deduplication.
4. Real-world: make a distributed job trigger safe under retries.

---

# Module 8 — Fault Tolerance Basics

## 1. Title

**Fault Tolerance Basics: Designing for Failure Instead of Assuming Success**

## 2. Who This Is For

- Backend engineers
- distributed systems learners
- reliability-minded designers

**Background needed**
- services
- replicas
- timeouts
- retries

## 3. Problem Definition

Systems fail:

- node crashes
- process restarts
- disks fail
- networks partition
- downstreams timeout

We need systems that degrade, not collapse.

## 4. First Principles Thinking

### Naive system

```
Client → API → DB
```

One DB. One API.

### Why it fails

Any single failure kills service.

### Naive diagram

```
Client → API → DB
             X
           outage
```

## 5. Build the Intuition (Step-by-Step)

### Step 1 — Remove single points of failure

```
LB → API1 API2 API3
```

### Step 2 — Add redundancy

```
Primary DB + replicas
```

### Step 3 — Add timeout + retry carefully

```
Caller waits forever? bad
Caller retries blindly? also bad
```

### Step 4 — Add circuit breaker / fallback

```
Downstream unhealthy
   ↓
Stop hammering it
```

## 6. Mental Model

### Fault tolerance layers

```
Failure happens
    ↓
Detect
    ↓
Isolate
    ↓
Retry or fallback
    ↓
Recover
```

### Invariants

- no single instance should be critical
- callers should not wait forever
- failures should be contained

## 7. Final System Design View for This Module

```
Users
  ↓
LB
  ↓
API Pool
  ↓
Cache / Queue / DB replicas
  ↓
Health checks + failover + retries + timeouts
```

## 8. Implementation Perspective

Techniques:
- health checks
- multi-AZ deployment
- replication
- timeouts
- bounded retries
- circuit breakers
- dead-letter queues

## 9. Walkthrough Example

Downstream email provider fails.

```
API → Queue → Email worker → Provider X
                               fails
```

Safe flow:

```
retry bounded
   ↓
fallback provider or DLQ
   ↓
system survives
```

## 10. Performance & Scalability

### Broken bottleneck

```
One failing dependency
       ↓
all callers block
       ↓
thread pool exhausted
       ↓
full outage
```

### Tolerant system

```
Failing dependency
      ↓
timeout
      ↓
circuit breaker
      ↓
fallback / isolate failure
```

## 11. Tradeoffs and Alternatives

More fault tolerance usually means:
- more complexity
- more duplicate infrastructure
- more cost

But less outage risk.

## 12. Common Mistakes

### Broken system diagram

```
Retry x infinite
      ↓
dependency overload
      ↓
retry storm
      ↓
bigger outage
```

## 13. Real-World Usage

Every serious production system:
- payments
- streaming
- cloud control planes
- messaging systems

## 14. Variations and Extensions

### Active-passive

```
Primary → standby
```

### Active-active

```
Region A + Region B live
```

## 15. Recap (Feynman Compression)

Fault tolerance means expecting parts to fail and designing the system to keep working anyway.

## 16. Exercises

1. Identify single points of failure in a simple API.
2. Add timeout and retry to a service call.
3. Intermediate: design email delivery with DLQ.
4. Real-world: make a multi-region API survive one-region failure.

---

# Module 9 — Backpressure

## 1. Title

**Backpressure: Preventing Fast Producers from Destroying Slow Consumers**

## 2. Who This Is For

- Engineers building async systems
- streaming / queue users
- interview candidates

**Background needed**
- queues
- producers/consumers
- overload basics

## 3. Problem Definition

When incoming work is faster than processing capacity:

```
producer rate > consumer rate
```

the backlog grows.

Without control:
- memory explodes
- queues grow forever
- latency becomes unbounded
- system crashes

## 4. First Principles Thinking

### Naive system

```
Producers → Queue → Workers
```

No limits.

### Why it fails

If workers can do 10K msgs/s and producers send 100K msgs/s:

```
backlog grows forever
```

### Naive diagram

```
[Fast producers] ───────────────→ [Queue] ─→ [Slow workers]
                     more in than out
```

## 5. Build the Intuition (Step-by-Step)

### Step 1 — Detect overload

```
Input > Processing
```

### Step 2 — Add bounded queue

```
Queue max size = N
```

### Step 3 — Apply policy when full

Options:
- reject
- shed low-priority traffic
- slow producers
- degrade features

### Step 4 — Add autoscaling

```
Backlog grows
   ↓
Scale workers
```

But note:
autoscaling is not infinite.

### Step 5 — Separate priority lanes

```
critical traffic
bulk traffic
```

## 6. Mental Model

### Water pipe model

```
Producer flow ─────→ buffer ─────→ consumer drain

If inflow > outflow too long:
buffer overflows
```

### Invariant

The system must have an explicit overload behavior.

## 7. Final System Design View for This Module

```
Producers
  ↓
Admission control / rate limit
  ↓
Bounded queue
  ↓
Workers
  ↓
Storage / downstreams
```

## 8. Implementation Perspective

Common controls:
- bounded queues
- rate limiting
- consumer lag monitoring
- retry budgets
- priority queues
- load shedding

## 9. Walkthrough Example

Notification campaign starts.

```
Producer rate = 200K/min
Worker capacity = 50K/min
```

Safe flow:

```
campaign traffic
   ↓
priority queue
   ↓
transactional traffic protected
bulk traffic delayed or throttled
```

## 10. Performance & Scalability

### Broken system diagram

```
No backpressure
     ↓
Queue grows
     ↓
memory pressure
     ↓
timeouts
     ↓
retry storm
     ↓
collapse
```

### Better system

```
Overload detected
     ↓
admission control
     ↓
bounded queue
     ↓
shed non-critical work
```

## 11. Tradeoffs and Alternatives

- rejecting work hurts immediate success rate
- not rejecting work may kill the whole system

Comparison:

```
No backpressure:
accept everything → collapse

With backpressure:
reject some → system survives
```

## 12. Common Mistakes

- unbounded queues
- retries without limits
- no priority separation
- scaling consumers without checking downstream capacity

## 13. Real-World Usage

- Kafka consumers
- API gateways
- streaming systems
- notification pipelines
- search indexing pipelines

## 14. Variations and Extensions

### Priority backpressure

```
critical lane stays open
bulk lane throttled
```

### Token-bucket admission + queue

```
burst allowed
sustained overload controlled
```

## 15. Recap (Feynman Compression)

Backpressure is how a system protects itself when work arrives faster than it can process it.

## 16. Exercises

1. Why are unbounded queues dangerous?
2. Add backpressure to an image processing pipeline.
3. Intermediate: protect transactional traffic during a bulk campaign.
4. Real-world: design overload control for a webhook delivery platform.

---

# Closing Visual Summary

```
System Design Decisions
        |
  ---------------------------------------------------------
  |        |          |          |         |        |      |
Reqs   Capacity   Lat/Thru    CAP     Scaling  State  Idempotency
                                                        |
                                               Fault Tolerance
                                                        |
                                                   Backpressure
```

## One-line intuition for each

- **Requirements**: know what matters before drawing boxes
- **Capacity**: rough math decides architecture shape
- **Latency vs Throughput**: optimize the right performance goal
- **CAP**: decide behavior under partition
- **Scaling**: grow bigger box or more boxes
- **State**: keep app layer stateless when possible
- **Idempotency**: make retries safe
- **Fault tolerance**: assume failures happen
- **Backpressure**: don’t let overload become collapse