# Mission-Critical Coding & Testing Checklist

## 🖥 Code-Writing Principles (CLEARFORM)

| Letter | Principle             | Example                                                                                         |
| ------ | --------------------- | ----------------------------------------------------------------------------------------------- |
| **C**  | Control complexity    | Keep functions short (<20 lines) and nesting ≤3; split long logic into smaller helpers          |
| **L**  | Limit dependencies    | Use built-ins before adding new packages; assess security and maintenance before adding         |
| **E**  | Eliminate duplication | Move repeated validation logic into a shared utility and test it once                           |
| **A**  | Avoid unused features | Don’t add config flags or endpoints until a real requirement exists                             |
| **R**  | Readable structure    | Use descriptive names like `processPayment()`; order code top-down from high-level to details   |
| **F**  | Fail fast, fail safe  | Validate all inputs and assumptions early fail immediately on invalid state and fail gracefully |
| **O**  | One job per module    | Keep payment processing separate from email sending                                             |
| **R**  | Reduce hidden state   | Avoid shared mutable globals; pass state explicitly as parameters                               |
| **M**  | Minimize side effects | Pure functions where possible; avoid unexpected DB writes in data transformation functions      |

---

## 🧪 Testing Principles (CIPHERBUD)

| Letter | Principle                    | Example                                                                                  |
| ------ | ---------------------------- | ---------------------------------------------------------------------------------------- |
| **C**  | Critical paths               | Test core flows like checkout end-to-end; simulate high load without losing transactions |
| **I**  | Inputs                       | For file upload: reject oversized, unsupported, empty, or corrupted files                |
| **P**  | Performance & baseline       | API baseline: p50=120 ms, p95=400 ms; fail build if p95 >500 ms after code changes       |
| **H**  | High concurrency             | Two users buying the last ticket; ensure one succeeds, one gets “sold out”               |
| **E**  | Edge cases                   | Username: empty, max length, emoji, special characters                                   |
| **R**  | Recovery after failure       | Payment processed but crash before confirmation; on restart, send confirmation or refund |
| **B**  | Backup & restore             | Verify last 24h backup; restore in staging and match table/row counts                    |
| **U**  | Upstream dependency handling | Payment gateway delay of 30s; retry or fail gracefully without freezing                  |
| **D**  | Debug visibility             | Log `OrderID=1234 created` with request/trace ID and step timings                        |
