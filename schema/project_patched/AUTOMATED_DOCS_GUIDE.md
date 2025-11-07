# Automated Documentation Management System

## Overview

This system provides **automated enforcement** of the VERSIONING_OPERATING_CONTRACT, ensuring all governance documents maintain:

✅ **Unique Identifiers** - Each document has a permanent `doc_key`  
✅ **Semantic Versioning** - Every change bumps version appropriately  
✅ **One Document Per PR** - Atomic changes with clear history  
✅ **Immutable Snapshots** - Git tags for every document version  
✅ **Runtime Auditing** - Every pipeline run logs active policy versions

## Components

### 1. Document Registry Builder (`scripts/build_doc_registry.py`)

**Purpose:** Scans repository and enforces unique `doc_key` identifiers

**Usage:**
```bash
# Validate and build registry
python scripts/build_doc_registry.py

# Check only (no output file)
python scripts/build_doc_registry.py --check-only

# Custom output location
python scripts/build_doc_registry.py --output custom_registry.json
```

**Output:** `.runs/doc-registry.json`
```json
{
  "OC_CORE": {
    "path": "docs/standards/OC_CORE.md",
    "semver": "1.3.0",
    "status": "active",
    "mfid": "blake3_abc123..."
  },
  "PIPELINE_POLICY": {
    "path": "docs/standards/PIPELINE_POLICY.md",
    "semver": "2.1.0",
    "status": "active",
    "mfid": "blake3_def456..."
  }
}
```

### 2. CI Validation (`.github/workflows/docs-guard.yml`)

**Triggers:** Every PR that modifies `.md` files in `docs/` or `plans/`

**Checks:**
1. ✓ **One-Document Rule** - Only one file changed per PR
2. ✓ **Front-Matter Validation** - All required fields present
3. ✓ **SemVer Bump** - Version increased appropriately
4. ✓ **PR Title Intent** - Conventional Commits match bump type
5. ✓ **Unique doc_key** - No duplicate identifiers

**Example Error Messages:**
```
❌ ERROR: Only one documentation file may be changed per PR
This PR modifies 2 files:
  • docs/standards/OC_CORE.md
  • docs/standards/PIPELINE_POLICY.md

Please split this PR into separate PRs, one per document.
```

### 3. Post-Merge Tagger (`.github/workflows/doc-tags.yml`)

**Triggers:** After merge to `main`

**Action:** Creates immutable git tags for each document version

**Tag Format:** `docs-{doc_key}-{semver}`

**Examples:**
- `docs-OC_CORE-1.3.0`
- `docs-PIPELINE_POLICY-2.1.0`
- `docs-R_PIPELINE_PHASE_01-1.0.0`

**Usage:**
```bash
# Checkout specific policy version
git checkout docs-OC_CORE-1.3.0

# List all versions of a document
git tag -l "docs-OC_CORE-*"

# View tag details
git show docs-OC_CORE-1.3.0
```

### 4. Runtime Version Snapshot (`scripts/get_doc_versions.py`)

**Purpose:** Extract current document versions for pipeline logging

**Usage:**
```bash
# Simple format (doc_key -> semver)
python scripts/get_doc_versions.py

# Full JSON format
python scripts/get_doc_versions.py --format json

# Ledger format (for append-only logs)
python scripts/get_doc_versions.py --format ledger

# Filter by status
python scripts/get_doc_versions.py --status active

# Save to file
python scripts/get_doc_versions.py --output .runs/policy_snapshot.json
```

**Integration with Pipeline:**
```python
# At start of pipeline run
from scripts.get_doc_versions import DocumentVersionExtractor

extractor = DocumentVersionExtractor()
extractor.scan_documents(status_filter='active')

# Log to run ledger
ledger_entry = extractor.to_ledger_entry()
append_to_ledger(ledger_entry)

# Now you can answer: "What policies were in force during run X?"
```

## Workflow Guide

### Creating/Updating a Document

#### Step 1: Create Branch
```bash
git checkout -b docs/OC_CORE/clarify-section-3
```

#### Step 2: Edit Document

Update the front-matter:
```yaml
---
doc_key: OC_CORE          # Never change this
semver: 1.3.1             # Bump from 1.3.0
status: active
effective_date: 2025-11-03
supersedes_version: 1.3.0  # Previous version
owner: Platform.Engineering
contract_type: policy
---
```

Update the change log:
```markdown
## Change Log (recent)

- **1.3.1** — 2025-11-03 — Clarified wording in section 3
- **1.3.0** — 2025-11-01 — Added new deployment requirement
- **1.2.2** — 2025-10-28 — Fixed typo in example
```

#### Step 3: Commit with Conventional Commit Format
```bash
git add docs/standards/OC_CORE.md
git commit -m "fix: Clarify wording in section 3 of OC_CORE"
```

Commit format determines required bump:
- `fix:` → PATCH (1.3.0 → 1.3.1)
- `feat:` → MINOR (1.3.0 → 1.4.0)
- `feat!:` → MAJOR (1.3.0 → 2.0.0)

#### Step 4: Create PR

```bash
git push origin docs/OC_CORE/clarify-section-3
```

Create PR with title: `fix: Clarify wording in section 3 of OC_CORE`

#### Step 5: CI Validation

The CI will automatically check:
- ✓ Only one document changed
- ✓ Front-matter is valid
- ✓ SemVer increased (1.3.0 → 1.3.1)
- ✓ PR title matches bump type (`fix:` = PATCH ✓)
- ✓ `doc_key` is unique

#### Step 6: Approval & Merge

Based on change type:
- **PATCH**: Any reviewer (same day)
- **MINOR**: Document owner (1-2 days)
- **MAJOR**: Owner + Compliance (3-5 days)

#### Step 7: Automatic Tagging

After merge, the system automatically:
1. Creates tag: `docs-OC_CORE-1.3.1`
2. Pushes to remote
3. Tag is now immutable snapshot

## SemVer Decision Tree

```
Does change break existing behavior?
├─ YES → MAJOR (X.0.0)
│   Examples:
│   • Remove approval gate
│   • Change required field
│   • Incompatible workflow change
│
└─ NO → Does it add new requirements?
    ├─ YES → MINOR (0.X.0)
    │   Examples:
    │   • Add new gate
    │   • Expand scope
    │   • New optional feature
    │
    └─ NO → PATCH (0.0.X)
        Examples:
        • Fix typo
        • Clarify wording
        • Update examples
```

## Special Rules

### Execution Contracts

Documents with `contract_type: execution_contract` have special rules:

- **Only MAJOR or PATCH allowed** (no MINOR)
- **MAJOR** = scope change (requires `contract-rebaseline` label)
- **PATCH** = editorial only (meaning unchanged)

### One-Document Rule

Why: Ensures atomic changes, clear version history, proper rollback

**Blocked:**
```
PR: Update policies
├─ docs/standards/OC_CORE.md
└─ docs/standards/PIPELINE_POLICY.md  ❌
```

**Allowed:**
```
PR: Update OC_CORE
└─ docs/standards/OC_CORE.md  ✓
```

### Supersedes Chain

Always set `supersedes_version` to previous version:

```yaml
# Version 1.3.1
supersedes_version: 1.3.0  # Previous version

# Version 1.3.0
supersedes_version: 1.2.2  # Previous version
```

This creates an audit trail:
```
1.0.0 → 1.1.0 → 1.2.0 → 1.2.1 → 1.2.2 → 1.3.0 → 1.3.1
```

## Troubleshooting

### Error: "Only one documentation file may be changed per PR"

**Solution:** Split PR into multiple PRs, one per document

```bash
# Create separate branches
git checkout -b docs/OC_CORE/update
git checkout -b docs/PIPELINE_POLICY/update

# Cherry-pick specific changes
git checkout docs/OC_CORE/update
git cherry-pick <commit-with-OC_CORE-changes>
```

### Error: "semver must increase"

**Solution:** Bump version in front-matter

```yaml
# Change from:
semver: 1.3.0

# To:
semver: 1.3.1  # or 1.4.0, or 2.0.0
```

### Error: "PR suggests BREAKING change but bump is minor"

**Solution:** Either:
1. Bump to MAJOR version, OR
2. Remove `!` from PR title

```bash
# Option 1: Bump version
semver: 2.0.0  # MAJOR bump

# Option 2: Change PR title
# From: feat!: Breaking change
# To:   feat: New feature
```

### Error: "Duplicate doc_key detected"

**Solution:** Each document needs unique `doc_key`

```yaml
# Change one of the conflicting documents:
doc_key: OC_CORE_V2  # Make it unique
```

## Integration with R_PIPELINE

### At Pipeline Startup

```python
from scripts.get_doc_versions import DocumentVersionExtractor

# Extract active policy versions
extractor = DocumentVersionExtractor()
extractor.scan_documents(status_filter='active')

# Create ledger entry
policy_snapshot = extractor.to_ledger_entry()

# Log to run metadata
run_metadata = {
    'run_id': current_run_id,
    'timestamp': datetime.utcnow().isoformat(),
    'policies_in_force': policy_snapshot['documents'],
    'policy_count': policy_snapshot['count']
}

# Write to .runs/{run_id}/metadata.json
write_run_metadata(run_metadata)
```

### Querying Historical Policies

```bash
# What policies were in force on 2025-10-15?
git checkout $(git rev-list -1 --before="2025-10-15" main)
python scripts/get_doc_versions.py

# What was OC_CORE version 1.2.0?
git checkout docs-OC_CORE-1.2.0
cat docs/standards/OC_CORE.md
```

## Summary

This system provides **automated, enforceable governance** with:

✅ **Zero-ambiguity identifiers** (doc_key)  
✅ **Automated version enforcement** (CI guards)  
✅ **Immutable history** (git tags)  
✅ **Runtime auditing** (policy snapshots)  
✅ **Atomic changes** (one document per PR)  

**Result:** Complete auditability and deterministic rollback for all governance documents.
