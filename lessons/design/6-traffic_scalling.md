# 🧠 Scaling Systems: Load Balancing, Reverse Proxies, CDNs & Global Distribution

---

# 2. Who This Is For

- Intermediate engineers building web systems
- Basic understanding of:
  - HTTP requests
  - servers and APIs

---

# 3. Problem Definition

### Real-world scenario

You deploy your API:

```
User → Server → DB
```

At first, it works.

Then:

- traffic increases
- server slows down
- users experience timeouts

---

### Example

```
10 users → OK
10,000 users → server crashes ❌
```

---

### Constraints

- global users
- latency < 100ms
- high availability required
- unpredictable traffic spikes

---

### Core Problem

👉 **How do we handle more users without breaking the system?**

---

# 🧠 4. First Principles Thinking

---

## Why does this problem exist?

Because:

👉 A single machine has limits  
👉 Network distance adds latency  
👉 Traffic is uneven  

---

## What breaks?

```
All users → 1 server ❌
```

---

## Naive System

```
        ┌─────────┐
Users → │ Server  │ → DB
        └─────────┘
```

---

## Failure Scenario

```
Users ↑↑↑
   ↓
Server overloaded ❌
```

---

## Why it fails at scale

- CPU limits
- memory limits
- network limits

---

# 🧭 5. Build the Intuition (Step-by-Step)

---

## Step 1 — Horizontal Scaling

---

### Idea

Add more servers

---

### Diagram

```
        ┌─────────┐
Users → │ Server1 │
        ├─────────┤
        │ Server2 │
        ├─────────┤
        │ Server3 │
        └─────────┘
```

---

### Problem

```
Users don't know which server to hit ❌
```

---

---

## Step 2 — Load Balancer

---

### Solution

Distribute traffic

---

### Diagram

```
          ┌────────────┐
Users →   │ Load Balancer │
          └────┬───────┘
        ┌──────┼──────┐
        ▼      ▼      ▼
     Server1 Server2 Server3
```

---

### Behavior

```
Request → LB → one server
```

---

### Strategies

- round robin
- least connections

---

### Insight

👉 evenly distributes load

---

---

## Step 3 — Reverse Proxy

---

### Problem

Need control layer before servers

---

### Reverse Proxy Role

```
Client → Proxy → Backend
```

---

### Diagram

```
User → Reverse Proxy → Servers
```

---

### Responsibilities

- routing
- SSL termination
- caching

---

### Visualization

```
User
 ↓
[Proxy]
 ↓
Servers
```

---

---

## Step 4 — CDN (Content Delivery Network)

---

### Problem

Users far from server → high latency

---

### Without CDN

```
User (Asia) → Server (US)
```

---

### With CDN

```
User → Edge Server → Origin
```

---

### Diagram

```
        ┌────────────┐
        │   Origin   │
        └────┬───────┘
     ┌───────┼────────┐
     ▼       ▼        ▼
  CDN1     CDN2     CDN3
     ▲
     │
   User
```

---

### Insight

👉 content served closer to user

---

---

## Step 5 — Geo Distribution

---

### Problem

Single region = single point of failure

---

### Solution

Multiple regions

---

### Diagram

```
         Global DNS
             │
   ┌─────────┼─────────┐
   ▼                   ▼
Region A           Region B
(Server cluster)   (Server cluster)
```

---

### Behavior

```
User routed to nearest region
```

---

### Insight

👉 improves latency + availability

---

# 🧠 6. Mental Model

---

## Layers of Scaling

```
Users
 ↓
CDN (edge)
 ↓
Load Balancer / Proxy
 ↓
Servers (scaled horizontally)
 ↓
Database
```

---

## Data Flow

```
User → CDN → LB → Server → DB
```

---

## Before vs After

---

### Before

```
User → Server ❌
```

---

### After

```
User → CDN → LB → Servers ✔
```

---

# 🏗️ 7. Final System Design

---

## System Diagram

```
             ┌────────────┐
             │   Client   │
             └────┬───────┘
                  ▼
           ┌──────────────┐
           │     CDN      │
           └────┬─────────┘
                ▼
        ┌──────────────┐
        │ Load Balancer│
        └────┬─────────┘
      ┌──────┼──────────┐
      ▼      ▼          ▼
   Server1 Server2   Server3
      │       │          │
      ▼       ▼          ▼
             Database
```

---

## Request Flow

```
1. User hits CDN
2. CDN serves or forwards
3. Load balancer routes
4. Server processes
5. DB accessed
```

---

## Data Flow

```
Edge → Routing → Processing → Storage
```

---

# 🔧 8. Implementation Perspective

---

## Technologies

- Load Balancer: NGINX / AWS ELB
- CDN: Cloudflare / Akamai
- Reverse Proxy: NGINX
- DNS: Route53

---

## Pseudo Flow

```
request():
    if CDN cache:
        return content

    server = loadBalancer.pick()

    return server.handle()
```

---

# 🧪 9. Walkthrough Example

---

### Request: GET /image.jpg

---

### Steps

```
1. User requests image
2. CDN checks cache
3. If hit → return
4. If miss → fetch origin
5. Cache at edge
```

---

### Visual Trace

```
User
 ↓
CDN (hit ✔)
 ↓
Response
```

---

# ⏱️ 10. Performance & Scalability

---

## Bottleneck Without Scaling

```
All traffic → 1 server ❌
```

---

## With Scaling

```
Traffic → LB → many servers ✔
```

---

## Diagram

```
Users
 ↓
LB
 ↓ ↓ ↓
S1 S2 S3
```

---

## Geo Scaling

```
Users → nearest region
```

---

# ⚖️ 11. Tradeoffs and Alternatives

---

## Single Server vs Distributed

```
Single:
Simple but fragile

Distributed:
Complex but scalable
```

---

## CDN vs No CDN

```
No CDN:
User → origin (slow)

With CDN:
User → edge (fast)
```

---

# ⚠️ 12. Common Mistakes

---

## 1. No Load Balancer

```
All traffic → one server ❌
```

---

## 2. No CDN

```
Global users → high latency ❌
```

---

## 3. Poor routing

```
Uneven load distribution ❌
```

---

## Broken System

```
Users → Server → crash ❌
```

---

# 🌍 13. Real-World Usage

- Netflix (global CDN + load balancing)
- Google (geo-distributed systems)
- Cloudflare (edge CDN)

---

# 🚀 14. Variations and Extensions

---

## Multi-Layer Load Balancing

```
Global LB → Regional LB → Servers
```

---

### Diagram

```
Global LB
   ↓
Regional LB
   ↓
Servers
```

---

## Edge Computing

```
Logic runs at CDN edge
```

---

# 🔁 15. Recap (Feynman Compression)

👉 Systems scale by:

- adding servers (horizontal scaling)
- distributing traffic (load balancing)
- controlling entry (reverse proxy)
- moving data closer (CDN)
- spreading globally (geo distribution)

---

# 🧩 16. Exercises

---

### Easy

1. Why is a load balancer needed?
2. What does a CDN solve?

---

### Intermediate

3. Design system for:
   - global users
   - static + dynamic content

---

### Real-World Challenge

4. Design system for:

- 1M users worldwide
- high availability
- low latency

👉 Include:
- load balancing
- CDN
- geo distribution