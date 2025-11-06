# Workflows (Happy Path)

1. **Author/Update doc** → commit doc + update Doc Card front‑matter (if needed).
2. **Open PR** → `docs.guard` runs: static lint, schema checks, acceptance stubs, uniqueness checks, one‑artifact rule.
3. **Merge to main** → `docs.registry.build` regenerates the registry; `docs.publish` builds the site; a **PUBLISH** event is written to the ledger; release notes are generated.
