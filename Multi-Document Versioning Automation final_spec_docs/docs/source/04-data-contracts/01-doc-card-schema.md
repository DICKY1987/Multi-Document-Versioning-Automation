# Doc Card Schema

```yaml
schema_version: 1
ulid: 01JC4ABCDXYZ...       # immutable
key: DOC_OPERATING_CONTRACT # human key, unique, never reused
semver: 1.3.0               # doc version
status: active              # active|deprecated
effective_date: 2025-11-06
path: docs/source/VERSIONING_OPERATING_CONTRACT.md
owners: ["docs@project"]
links:
  delivers: ["DEL-DOCS-MGMT"]        # PBS leaf
  acceptance: ["AC-DOCS-001"]        # executable acceptance id
  evidence: ["reports/docs-validate.xml"]
card_version: 2                        # metadata revisions only
```
