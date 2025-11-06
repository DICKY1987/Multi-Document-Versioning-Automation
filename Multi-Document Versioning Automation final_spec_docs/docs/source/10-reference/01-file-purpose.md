# Key Artifacts & Deliverables

* **ARCHITECTURE.md** — high‑level system design & flows. *Deliverable:* Architecture doc.
* **AUTOMATED_DOCS_GUIDE.md** — operator & contributor handbook. *Deliverable:* Guide (user‑facing).
* **VERSIONING_OPERATING_CONTRACT.md** — governance rules for doc semver, tagging, change control. *Deliverable:* Operating contract.
* **IMPLEMENTATION_CHECKLIST.md** — DoR/DoD checklists for releases. *Deliverable:* Gate checklist.
* **IMPLEMENTATION_SUMMARY.md** — concise release notes & deltas.
* **Document Versioning AutomationREADME.md** — module readme for fast onboarding.
* **doc-tags.yml** — controlled vocabulary & facets used by `docs.tag`. *Deliverable:* Taxonomy config.
* **docs-guard.yml** — policy bundle (one‑artifact rule, coverage %, linkcheck budgets) loaded by `docs.guard`. *Deliverable:* Policy‑as‑code.
* **specs/contracts/plugin.contract.v1.json** — global contract definition (schemas, error semantics) all plugins must honor. *Deliverable:* Source of truth.
* **specs/schemas/*.schema.json** — JSON Schemas for Cards, Ledger, Registry, plugin I/O. *Deliverable:* Validated contracts.
* **ids/docs/cards/<ULID>.yaml** — Doc Cards, authoritative identity & metadata. *Deliverable:* Identity record.
* **.ledger/docs.jsonl** — append‑only events proving history. *Deliverable:* Provenance ledger.
* **registry/docs.registry.yaml** — generated index for fast lookups & audit joins. *Deliverable:* Registry.
* **docs/source/** — primary docs content (Markdown/MDX). *Deliverable:* Published content.
* **plan/pbs.yaml** — PBS of documentation products (outputs). *Deliverable:* PBS.
* **plan/deliverables/DEL-DOCS-MGMT.yaml** — DDS with acceptance & evidence. *Deliverable:* Executable acceptance.
* **plan/file-map.yaml** — map docs ↔ cards ↔ tests. *Deliverable:* Traceable file plan.
* **plan/rtm.yaml** — Requirements/Deliverables ↔ Tests ↔ Evidence. *Deliverable:* RTM.
* **plugins/docs/*** — plugin implementation folders (each with `manifest.yaml`, `src/*`, `schemas/*`, `tests/*`, `examples/*`), plus conformance tests. *Deliverable:* Extensible capabilities.
* **scripts/get_doc_versions.py** — utility used by `docs.version.bump` to compute new semver from diffs/policy. *Deliverable:* Semver tool.
* **scripts/build_doc_registry.py** — batch compile registry from Cards. *Deliverable:* Registry builder.
* **scripts/example_integration.py** — sample embedding of the SDK into other tooling.
* **tests/** — L0‑L3 test packs (contract, behavior, unit). *Deliverable:* Proof.
* **.github/workflows/** — PR guard, post‑merge registry, release/publish pipelines. *Deliverable:* Automated CI/CD.

> **All other files** (e.g., diagram sources, templates) live under `docs/source/` and are discovered by `docs.scan`.
