# Failure Isolation & Recovery Policy (issue 25)

This policy describes strategies for isolating failures in plugins
and recovering gracefully. It applies to all operations and the
kernel.

## Crash Containment

* Each plugin runs in its own process or thread to prevent crashes
  from propagating. The kernel monitors plugin processes and
  restarts them with exponential backoff.
* A plugin crash triggers an `id.state_changed` event recorded in
  the ledger.

## Error Propagation

* Operation handlers must return structured errors per the shared
  error contract. Unhandled exceptions are converted to error
  objects and logged at the `error` level with stack traces.

## Quarantine & Disable

* A plugin that fails repeatedly (more than three times within a
  minute) is automatically disabled and marked as `invalid` in
  the registry. An alert is sent to maintainers.

## Retry & Backoff

* Network operations should implement exponential backoff with
  jitter. Maximum attempts default to 5; override via config.

## Logging Standards

* All failures must include the `event_id`, `op_key`, and
  relevant identifiers. Sensitive data must be redacted.