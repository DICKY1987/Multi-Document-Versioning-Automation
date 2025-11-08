# System Architecture

## Complete Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DOCUMENTATION LIFECYCLE                          │
└─────────────────────────────────────────────────────────────────────┘

1. DOCUMENT CREATION/UPDATE
   ┌──────────────┐
   │  Developer   │
   │  edits doc   │
   └──────┬───────┘
          │
          ↓
   ┌──────────────────────────────┐
   │  Add/Update Front-Matter     │
   │  ─────────────────────────   │
   │  doc_key: OC_CORE           │  ← Unique, permanent ID
   │  semver: 1.3.1              │  ← Bump version
   │  status: active             │
   │  effective_date: 2025-11-03 │
   │  owner: Platform.Engineering│
   │  contract_type: policy      │
   └──────────────────────────────┘
          │
          ↓
   ┌──────────────────────────────┐
   │  Conventional Commit         │
   │  fix: Clarify section 3      │  ← Intent determines bump
   └──────────────────────────────┘
          │
          ↓
   ┌──────────────────────────────┐
   │  Create PR (1 doc only!)     │
   └──────────────────────────────┘

2. CI VALIDATION (docs-guard.yml)
   ┌──────────────────────────────┐
   │  PR Opened/Updated           │
   └──────┬───────────────────────┘
          │
          ↓
   ┌──────────────────────────────┐
   │  ✓ One-Document Rule         │  ← Only 1 file changed?
   └──────┬───────────────────────┘
          │
          ↓
   ┌──────────────────────────────┐
   │  ✓ Front-Matter Validation   │  ← All required fields?
   └──────┬───────────────────────┘
          │
          ↓
   ┌──────────────────────────────┐
   │  ✓ SemVer Bump Check         │  ← Version increased?
   └──────┬───────────────────────┘
          │
          ↓
   ┌──────────────────────────────┐
   │  ✓ PR Title Intent           │  ← fix:/feat:/feat!:
   └──────┬───────────────────────┘
          │
          ↓
   ┌──────────────────────────────┐
   │  ✓ Unique doc_key            │  ← No duplicates?
   └──────┬───────────────────────┘
          │
          ↓
   ┌──────────────────────────────┐
   │  Build doc-registry.json     │
   └──────┬───────────────────────┘
          │
          ├─ PASS ──→ Ready for review
          │
          └─ FAIL ──→ Block merge with clear error

3. HUMAN REVIEW
   ┌──────────────────────────────┐
   │  Approval Based on Type      │
   │  ─────────────────────────   │
   │  PATCH: Any reviewer         │
   │  MINOR: Document owner       │
   │  MAJOR: Owner + Compliance   │
   └──────┬───────────────────────┘
          │
          ↓
   ┌──────────────────────────────┐
   │  Merge to main               │
   └──────┬───────────────────────┘

4. POST-MERGE AUTOMATION (doc-tags.yml)
   ┌──────────────────────────────┐
   │  Detect Changed Documents    │
   └──────┬───────────────────────┘
          │
          ↓
   ┌──────────────────────────────┐
   │  Extract doc_key + semver    │
   │  Example: OC_CORE, 1.3.1     │
   └──────┬───────────────────────┘
          │
          ↓
   ┌──────────────────────────────┐
   │  Create Git Tag              │
   │  docs-OC_CORE-1.3.1          │  ← Immutable snapshot
   └──────┬───────────────────────┘
          │
          ↓
   ┌──────────────────────────────┐
   │  Push Tag to Remote          │
   └──────────────────────────────┘

5. RUNTIME INTEGRATION
   ┌──────────────────────────────┐
   │  Pipeline Run Starts         │
   └──────┬───────────────────────┘
          │
          ↓
   ┌──────────────────────────────┐
   │  get_doc_versions.py         │  ← Extract active policies
   └──────┬───────────────────────┘
          │
          ↓
   ┌──────────────────────────────┐
   │  Create Policy Snapshot      │
   │  {                           │
   │    "OC_CORE": "1.3.1",       │
   │    "PIPELINE_POLICY": "2.1.0"│
   │  }                           │
   └──────┬───────────────────────┘
          │
          ↓
   ┌──────────────────────────────┐
   │  Log to Run Ledger           │
   │  .runs/{run_id}/metadata.json│
   └──────────────────────────────┘
          │
          ↓
   ┌──────────────────────────────┐
   │  Execute Pipeline Tasks      │
   └──────┬───────────────────────┘
          │
          ↓
   ┌──────────────────────────────┐
   │  Run Complete                │
   │  (policies logged)           │
   └──────────────────────────────┘

6. AUDIT & ROLLBACK
   ┌──────────────────────────────┐
   │  Query: What policies were   │
   │  active during run X?        │
   └──────┬───────────────────────┘
          │
          ↓
   ┌──────────────────────────────┐
   │  Read run metadata           │
   │  .runs/{run_id}/metadata.json│
   └──────┬───────────────────────┘
          │
          ↓
   ┌──────────────────────────────┐
   │  Shows: OC_CORE v1.3.1       │
   └──────┬───────────────────────┘
          │
          ↓
   ┌──────────────────────────────┐
   │  Checkout that version       │
   │  git checkout docs-OC_CORE-1.3.1│
   └──────────────────────────────┘
          │
          ↓
   ┌──────────────────────────────┐
   │  Exact policy content        │
   │  from that moment            │
   └──────────────────────────────┘
```

## Key Enforcement Points

### ✅ CI Validation (Automated)
- One document per PR
- Valid front-matter
- Correct SemVer bump
- Unique doc_key identifiers
- PR title matches intent

### ✅ Post-Merge (Automated)
- Create immutable git tags
- Format: docs-{doc_key}-{semver}
- Pushed to remote

### ✅ Runtime (Integrated)
- Capture active policies
- Log to run metadata
- Enable historical queries

### ✅ Human Review (Manual)
- PATCH: Fast approval
- MINOR: Owner approval
- MAJOR: Owner + Compliance

## Data Flow

```
Document Source (Markdown)
         ↓
  Front-Matter Extraction
         ↓
  ┌──────────────┐
  │ doc_key      │ ──→ Registry uniqueness check
  │ semver       │ ──→ Version validation
  │ status       │ ──→ Active/deprecated filter
  │ owner        │ ──→ CODEOWNERS matching
  └──────────────┘
         ↓
  Git Tag: docs-{doc_key}-{semver}
         ↓
  Run Ledger: Policy snapshot
         ↓
  Audit Trail: Complete history
```

## Security Model

```
┌─────────────────────────────────────┐
│  Branch Protection (GitHub)         │
│  ─────────────────────────────      │
│  • Require status checks            │
│  • Require PR reviews               │
│  • No direct pushes to main         │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  CI Enforcement (GitHub Actions)    │
│  ─────────────────────────────      │
│  • One-document validation          │
│  • Front-matter validation          │
│  • SemVer validation                │
│  • Uniqueness validation            │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  Human Review (CODEOWNERS)          │
│  ─────────────────────────────      │
│  • Owner approval for MINOR/MAJOR   │
│  • Compliance for MAJOR             │
│  • Fast track for PATCH             │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  Immutable Tags (Git)               │
│  ─────────────────────────────      │
│  • Auto-created post-merge          │
│  • Cannot be modified               │
│  • Enables deterministic rollback   │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  Append-Only Ledger (Run Logs)      │
│  ─────────────────────────────      │
│  • Policy snapshot per run          │
│  • Complete audit trail             │
│  • Tamper-evident history           │
└─────────────────────────────────────┘
```

## Benefits Summary

| Feature | Implementation | Benefit |
|---------|----------------|---------|
| Unique IDs | `doc_key` in front-matter | No ambiguity, stable references |
| SemVer | Validated by CI | Clear change semantics |
| One-doc rule | CI enforcement | Atomic changes, clean history |
| Git tags | Auto-created | Immutable snapshots |
| Policy snapshots | Runtime capture | Full auditability |
| Conventional commits | PR title validation | Intent clarity |
| CODEOWNERS | GitHub native | Proper approval gates |

This architecture ensures **complete auditability** with **minimal manual overhead**.
