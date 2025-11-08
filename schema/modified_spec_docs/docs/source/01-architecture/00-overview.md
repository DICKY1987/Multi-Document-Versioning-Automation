# Architecture & Scope

## Purpose & Scope

This module builds, validates, versions, and publishes all project documentation as **docs-as-code**, using a **micro-kernel + plugins** architecture with **contract-first** manifests, **conformance tests**, and **deterministic IDs**. It enforces product-based planning (PBS→DDS→RTM), acceptance-test-driven docs, and immutable provenance via an append-only ledger.

### Goals

* Treat every doc as a versioned product with a **Deliverable Definition Sheet (DDS)**, executable acceptance, and traceability to tests and evidence. 
* Enforce **contract-first** interfaces for plugins (schemas, inputs/outputs, policies). 
* Guarantee **deterministic identity** (ULID + stable human key) with **Cards → Ledger → Registry** pattern. 
* Provide **no-judgment CI gates** (static→contract→behavior→perf→security) with auto-publish on green. 

### Non-Goals

* Not a general CMS; it assumes docs live in Git and are built headlessly.
* Not a translation platform (can integrate later via plugin).
