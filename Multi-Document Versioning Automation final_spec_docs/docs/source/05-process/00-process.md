# Process & Decision Artifacts

The system defines explicit process control and decision artifacts to drive deterministic, auditable flows.

## BPMN Process

The BPMN located in `/process/process.bpmn` outlines the high‑level workflow:

Author Edit → PR Opened → docs.guard → (Fail → Fix & Re‑run) | (Pass → Merge) → registry.build → publish → **PUBLISH** event.

## Decision Tables (DMN)

Decision tables in `/process/decisions.dmn` encode the SemVer bump rules, one‑artifact policy, and other policy escalations in a declarative way.

## Tailoring

Configuration in `/process/process-tailoring.yaml` defines feature flags (e.g., `enforce_one_artifact: true`), path roots, and allowed doc types to tailor the process to a specific repository.
