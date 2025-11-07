# Micro‑kernel & Plugins

## Architecture Overview

Core pattern: Doc Card (committed) → Doc Ledger (append-only) → Doc Registry (generated). The kernel provides discovery, schema validation, and orchestration. Plugins implement discrete capabilities with **JSON in/out** contracts and **manifested** capabilities.

### Module Boundaries

* Inputs: Markdown/MDX, diagrams (Mermaid/Draw.io), YAML/JSON specs, DDS files, tag configs.
* Outputs: Built site (HTML/PDF), registries, reports, badges, release notes, artifacts.

### Extension Points (plugin keys)

* docs.scan discover files & map to deliverables (PBS/DDS aware).
* docs.parse normalize front‑matter; extract titles/tags; compute doc hash.
* docs.validate schema/links/lint; enforce **DDS acceptance** presence.
* docs.version.bump semver policy & **immutability** of doc identity.
* docs.tag apply taxonomy from doc-tags.yml.
* docs.registry.build compile fast lookup & RTM edges.
* docs.publish build+push site and artifacts.
* docs.guard PR gate (one‑artifact rule, schema, uniqueness, coverage).
* docs.export.* CSV/JSON/MD exports for audit.

All plugins follow a **Plugin Manifest** (capabilities, contract range, config schema) and ship a **Conformance Test Pack** (fixtures + L0‑L3 tests).
