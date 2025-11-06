# Data Contract Addenda

## Doc Card Additions

* `doc_type` (enum): `"template" | "contract" | "plan" | "guide" | "standard" | "reference" | "policy"`.
* `deprecated_date` (date) and `deprecation_reason` (string): required when `status` is `deprecated`.
* `mfid` object:
  * `algo`: `blake3` (default) or `sha256`.
  * `digest`: hex string.
  * `normalized`: boolean (default `true`) indicating canonicalization before hashing.

## Ledger Event Additions

New event types and payloads:

* `CREATE`: `{ "initial_semver": "x.y.z" }`
* `REKEY`: `{ "old_key": "...", "new_key": "..." }`
* `DEPRECATE`: `{ "reason": "...", "deprecated_date": "YYYY-MM-DD" }`
* `CONSOLIDATE`: `{ "target_ulid": "ULID", "sources": ["ULID", ...] }`
* `MFID_UPDATE`: `{ "algo": "...", "digest": "...", "normalized": true }`

These augment the existing event schema.

## Registry Canonicalization & Drift

The canonical registry at `registry/registry.yaml` is a flat map keyed by `doc_key`.  A secondary view by ULID may be generated.  CI enforces that the registry is **generated**; manual edits fail without a generator delta and passing conformance tests.
