You are an expert software engineer, system architect, and technical educator.

The tutorial must:

* be technically correct and aligned with modern industry practices
* reflect real-world systems and constraints (not just theory)
* teach from first principles (not memorization)
* build strong intuition and decision-making ability
* prioritize **visual understanding over long explanations**

---

## 🎯 PRIMARY GOAL

By the end of this tutorial, the reader should be able to:

1. Understand the problem this design solves
2. Explain the system from first principles
3. Visualize how the system works end-to-end
4. Make informed design decisions and tradeoffs
5. Apply the concept to real-world systems
6. Adapt the design under constraints

---

## 🧩 STRUCTURE (FOLLOW EXACTLY)

### 1. Title

Clear and specific.

---

### 2. Who This Is For

* skill level
* required background

---

### 3. Problem Definition

* describe the real-world problem
* include a concrete example
* define constraints (scale, latency, etc.)

---

## 🧠 4. First Principles Thinking

Explain:

* Why does this problem exist?
* What breaks without this system?
* What does a naive solution look like?
* Why does it fail at scale?

👉 MUST include a **simple diagram or flow** of the naive approach.

---

## 🧭 5. Build the Intuition (Step-by-Step)

Derive the solution gradually:

* naive → improved → scalable
* explain each step

👉 For EACH step:

* include a **visual diagram or flow**
* show how the system evolves

DO NOT jump to final architecture.

---

## 🧠 6. Mental Model (MANDATORY VISUALIZATION)

Explain:

* how data flows
* what components exist
* what invariants are maintained

👉 MUST include:

* flow diagrams
* component diagrams
* before/after comparisons

Use ASCII diagrams if needed.

---

## 🏗️ 7. Final System Design

Present the architecture:

👉 MUST include:

* system diagram
* request flow
* data flow

Explain clearly:

* components
* interactions
* responsibilities

---

## 🔧 8. Implementation Perspective

Translate into real-world systems:

* technologies (optional)
* how engineers actually build it

👉 Include:

* simplified pseudo-flows or sequence diagrams

---

## 🧪 9. Walkthrough Example

Take one real request:

👉 MUST include:

* step-by-step flow
* visual trace of request through system

---

## ⏱️ 10. Performance & Scalability

Explain:

* bottlenecks
* scaling strategy

👉 MUST include:

* diagrams showing bottlenecks
* diagrams showing scaled system

---

## ⚖️ 11. Tradeoffs and Alternatives

Explain:

* when to use
* when not to use

👉 MUST include:

* comparison diagrams (e.g., cache vs no cache)

---

## ⚠️ 12. Common Mistakes

* typical failures

👉 MUST include:

* “broken system” diagrams
* what goes wrong visually

---

## 🌍 13. Real-World Usage

* where this appears in real systems

---

## 🚀 14. Variations and Extensions

* alternative architectures
* scaling improvements

👉 Include diagrams for variations

---

## 🔁 15. Recap (Feynman Compression)

Explain simply:

* what the system does
* how it works

---

## 🧩 16. Exercises

* 2 simple
* 1 intermediate
* 1 real-world challenge

---

## 🧠 CRITICAL RULE (MOST IMPORTANT)

For every abstract concept, you MUST:

👉 Replace or support explanation with a **diagram**

If a concept is:

* abstract
* system-level
* flow-based

Then:
❌ Do NOT explain it with text alone
✅ You MUST visualize it

---

## 🧠 LEARNING DESIGN RULES

* First Principles Thinking
* Feynman Technique
* Progressive Disclosure
* Visual-first explanation
* Worked Example + Variation

---

## ⚙️ TECHNICAL REQUIREMENTS

* realistic architecture
* practical decisions
* modern best practices

---

## 🚫 DO NOT:

* rely on long paragraphs
* explain without diagrams
* jump to final architecture
* use buzzwords without explanation

---

## OUTPUT QUALITY

The tutorial should feel like:

* a whiteboard session with a senior engineer
* not a blog post
* not documentation
* but a **visual reasoning walkthrough**

---


Your task is to create a **high-quality, deeply structured system design tutorial** about the following topics:


-- TOPIC HERE --

Now create the tutorial and format it inside 4 backticks to avoid leaking markdown format outside

Illustrate with simple drawing lines, and shapes inside the markdown if necessary.


----


## 🔥 Core Decision-Making (MOST IMPORTANT)
- [ ] Requirements Clarification (functional vs non-functional)
- [ ] Capacity Estimation (rough calculations)
- [ ] Latency vs Throughput
- [ ] Consistency vs Availability (CAP tradeoffs)
- [ ] Scalability (vertical vs horizontal)
- [ ] Stateless vs Stateful Design
- [ ] Idempotency
- [ ] Fault Tolerance Basics
- [ ] Backpressure

---

## 🧠 Data & Storage (VERY HIGH IMPACT)
- [ ] Data Modeling (tables, entities, relationships)
- [ ] SQL vs NoSQL (decision criteria)
- [ ] Indexing (core concept)
- [ ] Transactions & Isolation Levels (conceptual)
- [ ] Replication (read replicas)
- [ ] Partitioning / Sharding
- [ ] Denormalization (when & why)
- [ ] Data Lifecycle (archiving, retention)

---

## ⚡ Caching & Performance (CRITICAL IN REAL SYSTEMS)
- [ ] Cache-Aside Pattern
- [ ] Write-Through / Write-Back
- [ ] Cache Invalidation (core problem)
- [ ] TTL Strategy
- [ ] Hot Keys / Hot Partitions
- [ ] Rate Limiting
- [ ] Load Shedding
- [ ] Batching & Pagination

---

## 🔄 Async & Workflows (VERY COMMON IN BACKENDS)
- [ ] Message Queues
- [ ] Pub/Sub
- [ ] Event-Driven Architecture
- [ ] Task Queues / Background Jobs
- [ ] Retry Strategies
- [ ] Dead Letter Queue (DLQ)
- [ ] At-Least-Once vs Exactly-Once
- [ ] Eventual Consistency

---

## 🌐 API & Service Design
- [ ] API Design (resource modeling)
- [ ] REST Concepts
- [ ] RPC / gRPC (when to use)
- [ ] API Versioning
- [ ] Authentication vs Authorization
- [ ] Service-to-Service Communication
- [ ] Timeouts & Retries
- [ ] Circuit Breaker Pattern

---

## 🚦 Traffic & Scaling
- [ ] Load Balancing (conceptual)
- [ ] Horizontal Scaling
- [ ] Reverse Proxy (basic role)
- [ ] CDN (when & why)
- [ ] Geo Distribution (basic idea)

---

## 🔍 Observability & Reliability (VERY IMPORTANT IN REAL JOBS)
- [ ] Logging
- [ ] Metrics
- [ ] Tracing
- [ ] Health Checks
- [ ] Alerting
- [ ] SLO / SLA Concepts
- [ ] Incident Handling Basics
- [ ] Backup & Recovery

---

## 🔐 Security (PRACTICAL)
- [ ] TLS / HTTPS Basics
- [ ] Authentication (tokens, sessions)
- [ ] Authorization (RBAC basics)
- [ ] Secrets Management
- [ ] Input Validation
- [ ] Abuse Prevention (rate limiting)

---

## 🧩 Architecture Patterns (USEFUL CONTEXT)
- [ ] Monolith vs Microservices
- [ ] Modular Monolith
- [ ] Event-Driven Architecture
- [ ] CQRS (basic idea)
- [ ] Multi-Tenant Systems

---

## 🎯 Real-World Decision Patterns (MOST IMPORTANT)
- [ ] When to use a cache
- [ ] When to use a queue
- [ ] When to denormalize
- [ ] When to shard
- [ ] When to split a service
- [ ] When NOT to use microservices
- [ ] Consistency tradeoff decisions
- [ ] Cost vs performance tradeoffs