# Taxonomy & Auto‑Index

Each Doc Card includes a `doc_type` field drawn from the controlled vocabulary:
`template`, `contract`, `plan`, `guide`, `standard`, `reference`, `policy`.  This taxonomy drives auto‑index generation.

An auto‑indexer produces `docs/INDEX.md` listing the latest version for each `doc_type`.  The indexer also checks link integrity: generation fails if a referenced tag is missing.
