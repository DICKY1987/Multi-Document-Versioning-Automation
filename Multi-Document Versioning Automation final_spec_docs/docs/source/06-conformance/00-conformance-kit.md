# Conformance Kit & Compatibility

Each plugin must ship a **conformance kit** comprising fixtures and tests:

* `/conformance/fixtures/**` — golden Cards/Registries/Ledger slices.
* `/conformance/tests/contract/*` — schema checks & error semantics.
* `/conformance/tests/behavior/*` — BDD Given/When/Then scenarios.
* `/conformance/tests/perf/*` — build‑time budget smoke tests.

CI runs the kit and produces `conformance/results.json`. A **compatibility matrix** ensures plugins operate across supported runtimes and contract versions. The matrix lives at `/ci/conformance-matrix.yaml` and may look like:

```yaml
runtime: { python: ["3.11","3.12"], os: ["ubuntu-latest","windows-latest"] }
contracts: { plugin: [">=1.0 <2.0"], card: [">=1.0 <2.0"] }
plugins: ["id.mint","id.rekey","id.deprecate","id.consolidate","id.mfid.update","id.registry.build","docs.migrate","id.validate","id.ledger.append"]
```

All matrix entries must be green for a release to proceed.
