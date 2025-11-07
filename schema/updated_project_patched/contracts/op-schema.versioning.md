# Op Schema Versioning Policy (issue 7)

This document sets out rules for versioning operation input/output
schemas. Each operation schema carries its own `x-metadata.semver`.
Changes must adhere to Semantic Versioning:

* **MAJOR**: Breaking changes to an input or output schema (e.g.
  removing a property, changing its type). Releasing a breaking
  change requires bumping the operation's semver MAJOR component
  and incrementing the plugin's MAJOR.
* **MINOR**: Backward‑compatible additions (e.g. adding optional
  properties). Requires a MINOR bump in both the operation schema
  and the plugin.
* **PATCH**: Corrections that do not change the contract (e.g.
  clarifying descriptions). Requires a PATCH bump.

Deprecation must be signaled via `status: deprecated` in
`x-metadata`. Deprecated schemas remain valid for at least one minor
version. Removal of deprecated schemas must be coordinated with
plugin deprecation policies.