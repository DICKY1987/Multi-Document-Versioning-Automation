# Repository Layout

A reference implementation is organized as follows:

```
auto-docs/
├─ ARCHITECTURE.md
├─ AUTOMATED_DOCS_GUIDE.md
├─ VERSIONING_OPERATING_CONTRACT.md
├─ IMPLEMENTATION_CHECKLIST.md
├─ IMPLEMENTATION_SUMMARY.md
├─ Document Versioning AutomationREADME.md
├─ doc-tags.yml
├─ docs-guard.yml
├─ specs/
│  ├─ contracts/
│  │  └─ plugin.contract.v1.json
│  └─ schemas/
│     ├─ doc_card.schema.json
│     ├─ doc_ledger_event.schema.json
│     ├─ doc_registry.schema.json
│     ├─ docs.scan.in.schema.json
│     ├─ docs.scan.out.schema.json
│     ├─ docs.validate.report.schema.json
│     └─ docs.publish.out.schema.json
├─ ids/
│  └─ docs/
│     └─ cards/
│        └─ <ULID>.yaml
├─ .ledger/
│  └─ docs.jsonl
├─ registry/
│  └─ docs.registry.yaml
├─ docs/
│  ├─ source/
│  │  ├─ index.md
│  │  ├─ guides/
│  │  │  ├─ authoring.md
│  │  │  └─ versioning.md
│  │  └─ standards/
│  │     └─ contracts.md
│  └─ site/                # build output (ignored by Git)
├─ plan/
│  ├─ pbs.yaml
│  ├─ file-map.yaml
│  ├─ rtm.yaml
│  └─ deliverables/
│     └─ DEL-DOCS-MGMT.yaml
├─ plugins/
│  └─ docs/
│     ├─ PLG_DOCS_SCAN/
│     │  ├─ manifest.yaml
│     │  ├─ README.md
│     │  ├─ src/scan.py
│     │  ├─ schemas/{in,out}.schema.json
│     │  ├─ examples/*.json
│     │  └─ tests/test_scan.py
│     ├─ PLG_DOCS_PARSE/
│     │  ├─ manifest.yaml
│     │  └─ src/parse.py
│     ├─ PLG_DOCS_VALIDATE/
│     │  ├─ manifest.yaml
│     │  ├─ src/validate.py
│     │  ├─ schemas/validate.report.schema.json
│     │  └─ tests/test_validate.py
│     ├─ PLG_DOCS_VERSION_BUMP/
│     │  ├─ manifest.yaml
│     │  └─ src/version_bump.py
│     ├─ PLG_DOCS_TAG/
│     │  ├─ manifest.yaml
│     │  └─ src/tag.py
│     ├─ PLG_DOCS_REGISTRY_BUILD/
│     │  ├─ manifest.yaml
│     │  └─ src/registry_build.py
│     ├─ PLG_DOCS_PUBLISH/
│     │  ├─ manifest.yaml
│     │  └─ src/publish.py
│     └─ PLG_DOCS_GUARD/
│        ├─ manifest.yaml
│        └─ src/guard.py
├─ scripts/
│  ├─ get_doc_versions.py
│  ├─ build_doc_registry.py
│  └─ example_integration.py
├─ tests/
│  ├─ behavior/
│  │  └─ docs_registry.feature
│  ├─ contract/
│  │  └─ test_manifests.py
│  └─ unit/
│     └─ test_version_bump.py
└─ .github/workflows/
   ├─ docs-guard.yml
   ├─ docs-post-merge.yml
   └─ docs-release.yml
```
