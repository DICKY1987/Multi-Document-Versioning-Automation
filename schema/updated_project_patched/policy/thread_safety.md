# Thread Safety & Shared State (issue 31)

Plugins must be written to be thread‑safe and avoid unsafe shared
state. This policy outlines the concurrency guidelines and
mechanisms to protect data integrity.

## Guidelines

* **No mutable module‑level globals:** All state must be stored in
  function scopes or passed explicitly.
* **Use concurrency primitives:** When shared state is necessary,
  use locks or other synchronization primitives provided by the
  runtime.
* **Stateless handlers:** Prefer pure functions for operation
  handlers; derive all outputs from inputs and configuration.
* **Atomic operations:** File writes or database updates must be
  atomic and idempotent to support retries.
* **Avoid side effects in getters:** Functions that read state
  should not mutate it.