# Threat Model (issue 17)

This document outlines the threat model for the modular plugin
architecture. It identifies assets, actors, and threats, and
establishes security goals. Use it as a living document and
update it as the system evolves.

## Assets

* Plugin artefacts (source code, schemas, manifests)
* Identity cards and registries
* Ledger data and run snapshots
* Credentials and secrets

## Actors

* Maintainers and developers
* CI/CD systems
* External consumers of plugins
* Malicious insiders or attackers

## Threats

| Threat                          | Mitigation                 |
|--------------------------------|----------------------------|
| Supply‑chain tampering         | SBOM, SLSA level 3+        |
| Secret leakage                 | Secrets policy, scanning   |
| Unauthorized state mutation    | State‑change safety rails  |
| Denial of service via large ops| Sharding & perf SLOs       |
| Data exfiltration via logs     | Redaction & retention      |

## Security Goals

1. **Integrity:** prevent unauthorized modification of artefacts.
2. **Confidentiality:** protect secrets and personal data.
3. **Availability:** ensure core services continue operating under
   expected load.
4. **Traceability:** maintain audit logs linking actions to actors.