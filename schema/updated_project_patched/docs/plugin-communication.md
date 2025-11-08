# Plugin-to-Plugin Communication (issue 32)

This document describes patterns for communication between plugins.

## Event Bus

Plugins should communicate indirectly via events. An emitting plugin
records an event in the ledger (e.g., `rules.evaluated`), and
receivers register handlers for those events via their
`plugin.spec.json`.

### Advantages
* Loose coupling between plugins
* Easy to add new subscribers without modifying emitters
* Ledger provides audit trail

## Direct Calls (to be avoided)

Direct invocation of one plugin's code by another is discouraged
because it creates tight coupling and versioning challenges. If
required, implement a **service** plugin that exposes a stable
operation contract and allow others to depend on it via
`depends_on`.

## Shared Data Structures

Use common schemas and contracts for shared data structures. The
`contracts/` directory should hold these definitions; plugins
reference them via `$ref`.