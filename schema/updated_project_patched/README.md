# Project Patch Summary

This patch introduces a set of baseline artifacts and policies to address
critical gaps identified in the "ID what's missing" analysis. Each
added file corresponds to a numbered issue from the gap list. The
structure adheres to the existing conventions of the plugin-based
system, enabling CI/CD pipelines to validate and enforce the
necessary constraints.

## Added Files

| Issue # | File Path | Description |
|-------:|-----------|-------------|
| 1 | `rules/propagation.map.yml` | Defines propagation rules for the `docs.propagate` operation. Used by the new plugin to update downstream documents when upstream specs change. |
| 1 | `plugins/docs.propagate/plugin.spec.json` | Minimal specification for a new `docs.propagate` plugin. This declares a single operation with its input/output schemas and allowed actions. |
| 2 | `contracts/error.contract.v1.json` | A shared error contract defining a simple, machine-readable error model. Plugins should reference this in their output schemas. |
| 3 | `contracts/compatibility.matrix.yaml` | A compatibility matrix capturing supported contract ranges and runtime environments per plugin. CI should use this to validate manifest declarations. |
| 4 | `policy/slsa.yml` | Supply‑chain security policy specifying a minimum SLSA level and requiring SBOM, provenance, and attestation. |
| 5 | `policy/secrets.yml` | Secrets management policy defining rotation, allowed prefixes, disallowed patterns, and enforcement of secret scanning in PRs. |

## Usage Notes

These files are stubs intended to seed the implementation. You will
need to provide implementations for the `docs.propagate` operation
input/output schemas (`schemas/docs.propagate.input.schema.json` and
`schemas/docs.propagate.output.schema.json`) and wire the plugin
into your CI workflows. Further work is required to address the
remaining gaps in the combined list.

Each file includes comments explaining its purpose and how to extend it.