---
---

# 🚀 **Mission Card** — Surviving High-Stakes Software Battles

---

## **Side A — Testing Excellence (BATTLE TEST)**

**Mnemonic:** _Battle test._

| Letter | Short Principle                  |                                                                 Why (plain) | Good example                                                                  | Bad example                                                        |
| ------ | -------------------------------- | --------------------------------------------------------------------------: | ----------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **B**  | **Boundaries** — test interfaces | Verify every place your system talks to something else so assumptions hold. | Run an automated check that the payment API returns the exact fields you use. | Only mock external APIs in unit tests and assume real API matches. |
| **A**  | **Algorithms & core logic**      |    Test the rules that must never be wrong (money, safety, business rules). | Unit tests ensure refunds never exceed original charges.                      | Rely only on full-system tests and miss a rounding bug.            |
| **T**  | **Throughput & tail latency**    |     Measure slowest responses (95th/99th percentiles) under realistic load. | Load test shows p95 < target × 0.8 (headroom).                                | Only check average response time; ignore long slow tails.          |
| **T**  | **Trace end-to-end**             | Follow one user action from start to finish to confirm all parts cooperate. | Place a test order and confirm it reaches billing and warehouse.              | Test only the order form UI; never verify downstream systems.      |
| **L**  | **Logging & observability**      |     Tests must produce useful logs/IDs so failures are diagnosable quickly. | Test failures include trace ID, timestamps, and error context.                | Failures show only “Error” with no logs or identifiers.            |
| **E**  | **Eliminate flakiness**          |                        Make tests deterministic so results repeat reliably. | Use fixed test data and freeze clocks in time-based tests.                    | Tests randomly pass/fail depending on timing or external load.     |
| **T**  | **Test recovery & failover**     |        Simulate failures and confirm the system recovers without data loss. | Kill a node and verify another takes over and no orders are lost.             | Never simulate crashes; discover failover bugs in production.      |
| **E**  | **Emergency backups & rollback** |          Practice restores and rollbacks so they actually work in a crisis. | Restore a production backup in test within target time.                       | Backups exist but have never been restored or verified.            |
| **S**  | **Stress the edges**             |               Try extreme, tiny, or malformed inputs to find boundary bugs. | Submit max-size uploads and huge lists; verify graceful handling.             | Only test normal inputs and fail on edge cases in production.      |
| **T**  | **Time budget with buffer**      |    Require better performance in tests than your promise to users (margin). | If SLA p95 = 200ms, assert p95 ≤ 160ms in tests.                              | Tests pass at exactly 200ms and production variance breaks SLA.    |

---

## **Side B — Code Quality Excellence (CODE SHIELD)**

| Letter | Principle                      | Quick Reminder                               | Real-World Mission Tip                                    |
| ------ | ------------------------------ | -------------------------------------------- | --------------------------------------------------------- |
| **C**  | Clarity over Cleverness        | Write code _anyone_ can understand tomorrow. | Avoid cryptic one-liners or over-abstraction.             |
| **O**  | Only What’s Needed             | Build just what solves today’s problem.      | Don’t build frameworks for problems that don’t exist yet. |
| **D**  | Design for Change              | Keep parts modular & replaceable.            | Isolate risky logic (like payments) behind adapters.      |
| **E**  | Eliminate Assumptions          | Validate inputs and states explicitly.       | Fail fast if API response isn’t as expected.              |
| **S**  | Single Responsibility          | One function/module = one job, done well.    | Separate parsing from sending notifications.              |
| **H**  | Handle Failures First          | Think about failures before happy path.      | Check file existence before reading to avoid crashes.     |
| **I**  | Instrument for Insight         | Add logs, metrics, traces — help debugging.  | Include correlation IDs and timings in logs.              |
| **E**  | Efficiency by Evidence         | Measure before optimizing.                   | Profile to find bottlenecks — optimize DB queries first.  |
| **L**  | Limit Risk via Tests           | Test critical paths thoroughly.              | Write idempotency tests for billing flow.                 |
| **D**  | Document the Why, not the What | Explain reasoning behind tricky decisions.   | “Why this algo? Handles streaming well.”                  |
