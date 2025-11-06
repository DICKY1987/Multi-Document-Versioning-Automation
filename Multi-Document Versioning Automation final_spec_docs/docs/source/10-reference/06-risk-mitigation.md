# Risk & Mitigation

* **Drift between docs and registry** → Block merges via `docs.guard` & BDD acceptance.
* **Identity churn** → Keys are never reused; renames become aliases; ULID is immutable.
* **Flaky validation** → Treat as bugs; stabilize tests before release.
