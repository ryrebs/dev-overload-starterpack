# 🧠 Designing Event-Driven Systems: Message Queues, Pub/Sub & Reliable Processing

---

# 2. Who This Is For

- Intermediate backend engineers
- Familiar with:
  - APIs
  - Databases
  - Basic distributed systems

---

# 3. Problem Definition

### Real-World Scenario

You run an e-commerce system.

User places an order:

```
POST /order
```

This triggers:

- payment processing
- inventory update
- email notification
- analytics logging

---

### Naive Implementation

```
Client → API → Payment → Inventory → Email → Analytics → Response
```

---

### Constraints

- latency < 200ms
- traffic spikes (10k orders/sec)
- partial failures happen
- services must be independent

---

### Problem

- slow response
- cascading failures
- tightly coupled services

---

# 🧠 4. First Principles Thinking

---

### Why does this problem exist?

Because:

👉 Work is **coupled**  
👉 Work is **synchronous**  
👉 Failures **propagate immediately**

---

### What breaks?

```
If Email fails → whole request fails ❌
```

---

### Naive Flow

```
Client
  ↓
 API
  ↓
Payment → Inventory → Email → Analytics
```

---

### Failure Scenario

```
Client
  ↓
 API
  ↓
Payment ✔
  ↓
Inventory ✔
  ↓
Email ❌ → entire request fails
```

---

### Why it fails at scale

- slow chain = high latency
- one failure blocks everything
- no isolation

---

# 🧭 5. Build the Intuition (Step-by-Step)

---

## Step 1 — Introduce Message Queue

### Idea:

Decouple producer and consumer.

---

### Flow

```
Client → API → Queue → Worker
```

---

### Diagram

```
        ┌─────────┐
Client →│   API   │
        └────┬────┘
             ▼
        ┌─────────┐
        │ Queue   │
        └────┬────┘
             ▼
        Worker
```

---

### Insight

👉 API becomes fast  
👉 Work moves async

---

## Step 2 — Multiple Consumers

### Problem:

One worker = bottleneck

---

### Solution

```
Queue → multiple workers
```

---

### Diagram

```
         Queue
       ┌───┬───┬───┐
       ▼   ▼   ▼   ▼
    Worker Worker Worker
```

---

👉 Parallel processing

---

## Step 3 — Pub/Sub Model

### Problem:

Multiple systems need same event

---

### Instead of:

```
API → Email
API → Analytics
API → Inventory
```

---

### Use Pub/Sub

```
API → Topic → Subscribers
```

---

### Diagram

```
         ┌─────────┐
         │  Topic  │
         └───┬─────┘
      ┌──────┼──────┐
      ▼      ▼      ▼
   Email  Analytics Inventory
```

---

👉 One event → many consumers

---

## Step 4 — Event-Driven Architecture

### Idea

System reacts to events instead of direct calls

---

### Flow

```
OrderCreated event
     ↓
Services react independently
```

---

### Diagram

```
        Event Bus
            │
     ┌──────┼──────┐
     ▼      ▼      ▼
 Payment Inventory Email
```

---

👉 Loose coupling  
👉 Independent scaling

---

## Step 5 — Task Queues / Background Jobs

### Use case

- sending emails
- image processing
- report generation

---

### Flow

```
API → Queue → Worker → Job executed
```

---

### Visualization

```
User Request
     ↓
 API (enqueue job)
     ↓
 Queue
     ↓
 Worker executes later
```

---

## Step 6 — Retry Strategies

### Problem

Workers fail

---

### Naive failure

```
Job → fails → lost ❌
```

---

### Retry Flow

```
Job → fail → retry → success
```

---

### Diagram

```
Queue → Worker
         ↓
       fail
         ↓
      retry (with delay)
```

---

### Strategies

- exponential backoff
- fixed retry
- jitter

---

## Step 7 — Dead Letter Queue (DLQ)

### Problem

Some jobs always fail

---

### Solution

Move to DLQ

---

### Diagram

```
Queue → Worker
         ↓
       fail (max retries)
         ↓
        DLQ
```

---

👉 Prevents infinite retries

---

## Step 8 — Delivery Guarantees

---

### At-Least-Once

```
Message delivered ≥ 1 times
```

---

### Diagram

```
Queue → Worker
        ↘ retry → duplicate possible
```

---

### Exactly-Once (hard)

```
Message processed exactly once
```

---

### Requires

- deduplication
- idempotency

---

### Visualization

```
Worker:
if (already_processed(id)):
    skip
```

---

## Step 9 — Eventual Consistency

### Problem

Systems update asynchronously

---

### Example

```
Order placed
Inventory updated later
```

---

### Diagram

```
Time →
Order:      ✔
Inventory:     ✔ (later)
```

---

👉 System temporarily inconsistent  
👉 Eventually consistent

---

# 🧠 6. Mental Model

---

## Components

```
[Producer] → [Queue/Event Bus] → [Consumers]
```

---

## Data Flow

```
1. Event created
2. Published to queue
3. Consumers process independently
```

---

## Invariants

- queue buffers work
- consumers are stateless
- processing must be idempotent

---

## Before vs After

### Before

```
API → Service A → Service B → Service C
```

---

### After

```
API → Queue → Services independently
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
            ┌──────────┐
            │   API    │
            └────┬─────┘
                 ▼
         ┌──────────────┐
         │ Event Bus    │
         └────┬─────────┘
      ┌───────┼─────────┐
      ▼       ▼         ▼
  Payment  Inventory  Email
```

---

## Request Flow

```
1. API receives request
2. Publishes event
3. Returns response immediately
4. Consumers process asynchronously
```

---

## Data Flow

```
Event → Queue → Consumers → Side effects
```

---

# 🔧 8. Implementation Perspective

---

## Example Stack

- Kafka / RabbitMQ / SQS
- Workers (Node, Python, Go)
- Redis (optional buffering)

---

## Pseudo Flow

```
publish(event):
    queue.send(event)

worker():
    event = queue.receive()
    process(event)
    ack()
```

---

## Idempotency Example

```
if db.exists(event_id):
    return

process()
db.save(event_id)
```

---

# 🧪 9. Walkthrough Example

---

### Order Placement

---

### Step-by-Step

```
1. User places order
2. API emits OrderCreated
3. Event bus distributes
4. Payment processes
5. Inventory updates
6. Email sent
```

---

### Visual Trace

```
User
 ↓
API
 ↓
Event Bus
 ↓   ↓   ↓
Pay Inv Email
```

---

# ⏱️ 10. Performance & Scalability

---

## Bottleneck Without Queue

```
API handles everything ❌
```

---

## With Queue

```
API → Queue → Workers scale horizontally
```

---

## Diagram

```
          Queue
       ┌───┬───┬───┐
       ▼   ▼   ▼   ▼
    Worker Worker Worker
```

---

👉 Scale by adding workers

---

# ⚖️ 11. Tradeoffs and Alternatives

---

## Sync vs Async

```
Sync:
API → Service → Response

Async:
API → Queue → Response
```

---

## Tradeoffs

| Approach | Pros | Cons |
|---------|------|------|
| Sync    | simple | slow, fragile |
| Async   | scalable | complex |

---

# ⚠️ 12. Common Mistakes

---

## 1. No Idempotency

```
Retry → duplicate effects ❌
```

---

## 2. Infinite Retries

```
Fail → retry → fail → retry forever ❌
```

---

## 3. No DLQ

```
Bad messages block queue ❌
```

---

## Broken System Diagram

```
Queue → Worker
         ↓
       fail
         ↓
      retry forever 🔁
```

---

# 🌍 13. Real-World Usage

- Kafka event streams
- Payment systems
- Notification systems
- Microservices communication

---

# 🚀 14. Variations and Extensions

---

## Fan-Out Pattern

```
Event → multiple queues
```

---

## Diagram

```
       Event
         │
   ┌─────┼─────┐
   ▼     ▼     ▼
 Queue Queue Queue
```

---

## Priority Queues

```
High priority processed first
```

---

## Diagram

```
[High] → Worker first
[Low ]
```

---

# 🔁 15. Recap (Feynman Compression)

We:

- decouple systems using queues
- process work asynchronously
- retry failures safely
- isolate bad messages (DLQ)
- accept eventual consistency

👉 Result: scalable, resilient system

---

# 🧩 16. Exercises

---

### Easy

1. Why is async faster than sync?
2. What problem does DLQ solve?

---

### Intermediate

3. Design retry strategy for payment failures

---

### Real-World Challenge

4. Design a system for:
   - 1M events/sec
   - multiple consumers
   - strict reliability

👉 Include:
- queue
- retries
- DLQ
- idempotency