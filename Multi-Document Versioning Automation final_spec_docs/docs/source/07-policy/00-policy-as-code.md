# Policy as Code

Policies are expressed as code under `/policy/`. Rules are implemented using OPA/Rego (or an equivalent engine) and include:

* One‑artifact rule and minimum coverage thresholds.
* SemVer mapping rules.
* Doc type allowlist (`doc_type`) and taxonomy constraints.
* MFID (content fingerprint) presence required on release.
* Forbidden MINOR bumps for specific contract types (if configured).

Each policy has positive and negative tests in `/policy/tests/**`. During CI, the **L5 gate** runs the policy bundle; any violations cause the PR to fail.
