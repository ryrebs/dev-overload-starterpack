---
---

# 🚀 **Mission Card** — Surviving High-Stakes Software Battles

---

## **Side A — Testing Excellence (RAPID TEST)**

**Mnemonic:** _RAPID TEST keeps the ship running._

| Letter | Principle                       | Why it Matters                               | Quick Example                     |
| ------ | ------------------------------- | -------------------------------------------- | --------------------------------- |
| **R**  | **Realistic Environments**      | Tests close to prod catch real issues early. | Ephemeral DB per CI run.          |
| **A**  | **Automate Everything**         | Manual testing is too slow for crises.       | CI/CD runs all tests on PR.       |
| **P**  | **Prioritize Critical Paths**   | Cover what breaks the business first.        | Single E2E for checkout.          |
| **I**  | **Isolate Tests**               | Avoid interference and flakiness.            | Scoped fixtures, no shared state. |
| **D**  | **Detect Flakiness Fast**       | Flaky tests erode trust.                     | Quarantine and fix root cause.    |
| **T**  | **Test Data is Deterministic**  | Same input = same output; aids debugging.    | Seed random values.               |
| **E**  | **Edge Cases Matter**           | Bugs hide at boundaries.                     | Empty list, max value, bad input. |
| **S**  | **Security Checks in Pipeline** | Vulnerabilities can sink you.                | SAST/DAST scans in CI.            |
| **T**  | **Trace & Log in Tests**        | Debug faster under pressure.                 | Correlation IDs in E2E runs.      |

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

