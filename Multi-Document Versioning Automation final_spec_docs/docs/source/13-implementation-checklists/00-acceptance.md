# Definition of Done

* 100% of Doc Cards map to existing files; 0 orphans both ways.
* DDS acceptance features pass in CI (green L2).
* Ledger receives `CREATE/UPDATE/PUBLISH` with run ULID for each change.
* Registry rebuilds clean; `by_ulid` and `by_key` are consistent.
* Docs site builds with no broken links; perf budgets respected.
* Policies in `docs-guard.yml` satisfied (coverage, one-artifact rule if enabled).
