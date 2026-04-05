# 🧠 Designing Secure Systems: TLS, Authentication, Authorization & Abuse Protection

---

# 2. Who This Is For

- Intermediate engineers building APIs / backend systems
- Basic knowledge of:
  - HTTP
  - APIs
  - Databases

---

# 3. Problem Definition

### Real-world scenario

You are building a public API:

```
POST /transfer-money
GET /user/profile
```

---

### Threats

- data interception
- unauthorized access
- malicious inputs
- abuse (spam, bots)

---

### Constraints

- millions of users
- internet-facing system
- latency < 100ms
- security must not break UX

---

### Core Problem

👉 **How do we ensure only the right users can access the system safely?**

---

# 🧠 4. First Principles Thinking

---

## Why does this problem exist?

Because:

👉 Internet is untrusted  
👉 Anyone can send requests  
👉 Data can be intercepted  

---

## What breaks without security?

```
Attacker → API → DB
```

---

## Naive System

```
User → API → DB
```

---

## Attack Scenario

```
Attacker intercepts request
Reads/modifies data ❌
```

---

## Why it fails

- no encryption
- no identity
- no permission control

---

# 🧭 5. Build the Intuition (Step-by-Step)

---

## Step 1 — TLS / HTTPS (Secure Transport)

---

### Problem

Data sent in plain text

---

### Without TLS

```
User → (plaintext) → Server
        ↑ attacker reads
```

---

### With TLS

```
User → (encrypted) → Server
        🔒
```

---

### Diagram

```
User
 ↓
[ ENCRYPTED CHANNEL 🔒 ]
 ↓
Server
```

---

### Insight

👉 Protects data in transit  
👉 Prevents eavesdropping  

---

---

## Step 2 — Authentication (Who are you?)

---

### Problem

Server doesn't know who user is

---

### Add Authentication

---

### Session-Based

```
Login → Server stores session
Client sends session_id
```

---

### Diagram

```
User → Login → Server
           ↓
      session_id

User → API (session_id)
```

---

### Token-Based (JWT)

```
User → Login → Token
User → API (token)
```

---

### Diagram

```
User → API
       │
       ▼
    [Token]
       │
    Verified
```

---

### Insight

👉 Authentication = identity

---

---

## Step 3 — Authorization (What can you do?)

---

### Problem

Authenticated user ≠ allowed action

---

### Example

```
User tries:
DELETE /admin
```

---

### RBAC (Role-Based Access)

---

### Diagram

```
User → Role → Permissions
```

```
Admin → can delete
User  → cannot delete
```

---

### Flow

```
Request → Auth → Role check → Allow / Deny
```

---

---

## Step 4 — Secrets Management

---

### Problem

Hardcoding secrets

```
API_KEY = "12345" ❌
```

---

### Proper Approach

```
App → Secret Manager → Secret
```

---

### Diagram

```
App
 ↓
Secret Manager
 ↓
Database password
```

---

### Insight

👉 Secrets must be stored securely and rotated

---

---

## Step 5 — Input Validation

---

### Problem

User sends malicious input

```
DROP TABLE users;
```

---

### Without Validation

```
User → API → DB (executes ❌)
```

---

### With Validation

```
User → Validate → API → DB
```

---

### Diagram

```
User Input
   ↓
[Validator]
   ↓
API
```

---

### Insight

👉 Never trust user input

---

---

## Step 6 — Abuse Prevention (Rate Limiting)

---

### Problem

Attackers spam requests

---

### Without Protection

```
Attacker → 100k requests → API crashes ❌
```

---

### With Rate Limiting

```
Attacker → limit → blocked
```

---

### Diagram

```
Request → [Rate Limiter]
             ↓
        allow / reject
```

---

### Insight

👉 Protect system capacity

---

# 🧠 6. Mental Model

---

## Security Layers

```
[Transport] → TLS
[Identity]  → Authentication
[Access]    → Authorization
[Input]     → Validation
[Abuse]     → Rate limiting
[Secrets]   → Secure storage
```

---

## Full Flow

```
User
 ↓
TLS (secure)
 ↓
Auth (who?)
 ↓
AuthZ (allowed?)
 ↓
Validation (safe?)
 ↓
Rate limit (abuse?)
 ↓
API → DB
```

---

## Before vs After

---

### Before

```
User → API → DB ❌
```

---

### After

```
User → TLS → Auth → AuthZ → Validation → API → DB ✔
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
        │ TLS (HTTPS)  │
        └────┬─────────┘
             ▼
        ┌──────────────┐
        │ Auth Layer   │
        └────┬─────────┘
             ▼
        ┌──────────────┐
        │ Authorization│
        └────┬─────────┘
             ▼
        ┌──────────────┐
        │ Validation   │
        └────┬─────────┘
             ▼
        ┌──────────────┐
        │ Rate Limiter │
        └────┬─────────┘
             ▼
        ┌──────────────┐
        │ API / Logic  │
        └────┬─────────┘
             ▼
        ┌──────────────┐
        │ DB / Secrets │
        └──────────────┘
```

---

## Request Flow

```
1. HTTPS handshake
2. Authenticate user
3. Check permissions
4. Validate input
5. Apply rate limit
6. Execute logic
```

---

## Data Flow

```
Encrypted → Verified → Authorized → Safe → Processed
```

---

# 🔧 8. Implementation Perspective

---

## Technologies

- TLS: HTTPS
- Auth: JWT / OAuth / Sessions
- AuthZ: RBAC middleware
- Secrets: Vault / AWS Secrets Manager
- Validation: schema validation (JSON schema)
- Rate limiting: Redis / API gateway

---

## Pseudo Flow

```
handleRequest(req):
    assert https

    user = authenticate(req.token)

    authorize(user, req.action)

    validate(req.input)

    rateLimiter.check(user)

    process()
```

---

# 🧪 9. Walkthrough Example

---

### Request: POST /transfer-money

---

### Steps

```
1. TLS secures connection
2. Token verified
3. Check user role
4. Validate amount
5. Rate limit check
6. Execute transfer
```

---

### Visual Trace

```
User
 ↓
TLS 🔒
 ↓
Auth
 ↓
AuthZ
 ↓
Validation
 ↓
Rate Limiter
 ↓
API → DB
```

---

# ⏱️ 10. Performance & Scalability

---

## Bottleneck

```
Security checks add latency
```

---

## Optimized System

```
Gateway handles:
- TLS
- Rate limiting
- Auth
```

---

### Diagram

```
Client → Gateway → Services
```

---

👉 Offload work to edge

---

# ⚖️ 11. Tradeoffs and Alternatives

---

## Token vs Session

```
Session:
Server stores state

Token:
Client stores state
```

---

## Diagram

```
Session:
Client → Server (lookup)

Token:
Client → verify locally
```

---

## Tradeoffs

| Approach | Pros | Cons |
|----------|------|------|
| Session  | secure | scaling harder |
| Token    | scalable | harder revoke |

---

# ⚠️ 12. Common Mistakes

---

## 1. No HTTPS

```
Plaintext traffic ❌
```

---

## 2. Trusting user input

```
SQL injection ❌
```

---

## 3. Missing authorization

```
User accesses admin ❌
```

---

## Broken System

```
User → API → DB
(no checks)
```

---

# 🌍 13. Real-World Usage

- Banking APIs (strict auth + TLS)
- SaaS platforms (multi-tenant RBAC)
- Public APIs (rate limiting + tokens)

---

# 🚀 14. Variations and Extensions

---

## Zero Trust Architecture

```
Every request verified
```

---

### Diagram

```
Service → Auth → Service
(no trust)
```

---

## API Gateway Pattern

```
Gateway handles security
```

---

### Diagram

```
Client → Gateway → Services
```

---

# 🔁 15. Recap (Feynman Compression)

👉 Secure system = layers:

- TLS → secure data
- Auth → who are you
- AuthZ → what can you do
- Validation → safe input
- Rate limit → prevent abuse
- Secrets → protect credentials

---

# 🧩 16. Exercises

---

### Easy

1. Why is HTTPS mandatory?
2. Difference between auth and authorization?

---

### Intermediate

3. Design RBAC for admin vs user system

---

### Real-World Challenge

4. Design API for:

- public access
- financial data
- high traffic

👉 Include:
- TLS
- auth
- RBAC
- rate limiting