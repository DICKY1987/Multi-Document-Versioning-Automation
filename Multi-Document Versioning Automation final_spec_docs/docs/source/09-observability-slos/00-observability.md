# Observability

Every plugin run emits an **OTel trace** (`plugin.key`, `subject.ulid`, `result`) with run ULID, uploaded as artifacts; local Jaeger/SigNoz for dev, console exporter in CI.

## SLOs

Default service level objectives:

* Registry build p95 latency < 2 seconds; error rate < 0.5%.
* Validation p95 latency < 1 second per file.
* Publish end‑to‑end < 5 minutes.

Breaches fail the performance gate and record a `PUBLISH_BLOCKED` annotation in the run ledger.
