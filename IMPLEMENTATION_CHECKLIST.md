# Implementation Checklist

Use this checklist to implement the automated documentation management system.

## Phase 1: Setup (15 minutes)

### Step 1: Copy Files to Repository
```bash
# From the outputs directory, copy to your repository
cp -r .github /path/to/your/repo/
cp -r scripts /path/to/your/repo/
cp -r examples /path/to/your/repo/
```

- [ ] Copied `.github/workflows/docs-guard.yml`
- [ ] Copied `.github/workflows/doc-tags.yml`
- [ ] Copied `scripts/build_doc_registry.py`
- [ ] Copied `scripts/get_doc_versions.py`
- [ ] Copied `examples/example_integration.py`

### Step 2: Make Scripts Executable
```bash
chmod +x scripts/*.py
chmod +x examples/*.py
```

- [ ] Made scripts executable

### Step 3: Test Scripts Locally
```bash
# Test registry builder
python scripts/build_doc_registry.py --check-only

# Test version extractor
python scripts/get_doc_versions.py
```

- [ ] Registry builder runs without errors
- [ ] Version extractor runs without errors

## Phase 2: CI Configuration (10 minutes)

### Step 4: Commit and Push Workflows
```bash
git checkout -b setup/docs-automation
git add .github/workflows/
git add scripts/
git add examples/
git commit -m "feat: Add automated documentation management system"
git push origin setup/docs-automation
```

- [ ] Created feature branch
- [ ] Committed files
- [ ] Pushed to remote

### Step 5: Merge to Main
```bash
# Create PR and merge (after review)
gh pr create --title "feat: Add docs automation" --body "Implements automated documentation management"
```

- [ ] Created PR
- [ ] Reviewed changes
- [ ] Merged to main

### Step 6: Configure Branch Protection
In GitHub Settings → Branches → main:

- [ ] ✅ Require status checks before merging
  - [ ] ✅ Check: `validate-docs`
- [ ] ✅ Require pull request reviews
  - [ ] Require approvals: 1
- [ ] ✅ Require branches to be up to date

### Step 7: Test CI
```bash
# Create test branch
git checkout -b test/docs-ci
echo "test" >> docs/test.md
git add docs/test.md
git commit -m "test: CI validation"
git push origin test/docs-ci

# Create PR - should trigger docs-guard workflow
```

- [ ] Created test PR
- [ ] CI workflow triggered
- [ ] Workflow completed (passed or failed as expected)

## Phase 3: Document Migration (30-60 minutes)

### Step 8: Identify Documents to Migrate
```bash
# Find all markdown files without front-matter
find docs/ plans/ -name "*.md" -type f
```

- [ ] Listed all documents
- [ ] Identified which need front-matter

### Step 9: Add Front-Matter Template
For each document, add to the top:

```yaml
---
doc_key: DOC_UNIQUE_ID           # Choose unique ID
semver: 1.0.0                    # Initial version
status: active                   # active | deprecated | frozen
effective_date: 2025-11-03       # Today's date
supersedes_version: null         # No previous version
owner: Platform.Engineering      # Owning team
contract_type: policy            # policy | intent | execution_contract
---
```

- [ ] Created migration plan (which docs, what doc_keys)
- [ ] Decided on naming convention for doc_keys

### Step 10: Migrate Documents (One PR per Document!)
```bash
# For EACH document:
git checkout -b docs/DOCNAME/add-versioning

# Add front-matter to ONE document
# Edit: docs/standards/OC_CORE.md

git add docs/standards/OC_CORE.md
git commit -m "feat: Add versioning to OC_CORE (initial migration)"
git push origin docs/DOCNAME/add-versioning

# Create PR, review, merge
# REPEAT for each document
```

- [ ] Document 1: _______________ (doc_key: _______) ✅
- [ ] Document 2: _______________ (doc_key: _______) ✅
- [ ] Document 3: _______________ (doc_key: _______) ✅
- [ ] Document 4: _______________ (doc_key: _______) ✅
- [ ] (Add more as needed)

### Step 11: Verify Tags Created
```bash
# After each merge, check tags
git pull --tags
git tag -l "docs-*"
```

- [ ] Tags created automatically after merge
- [ ] Tag format: `docs-{doc_key}-{semver}` ✅

## Phase 4: R_PIPELINE Integration (30 minutes)

### Step 12: Add Policy Snapshot to Pipeline Startup
```python
# In your pipeline startup code:
from scripts.get_doc_versions import DocumentVersionExtractor

def start_pipeline_run(run_id):
    # Create run directory
    run_dir = Path('.runs') / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    
    # Capture policy snapshot
    extractor = DocumentVersionExtractor()
    extractor.scan_documents(status_filter='active')
    
    # Save snapshot
    snapshot = extractor.to_ledger_entry()
    with open(run_dir / 'policy_snapshot.json', 'w') as f:
        json.dump(snapshot, f, indent=2)
    
    # Log to ledger
    append_to_ledger(run_dir / 'ledger.jsonl', snapshot)
    
    return snapshot
```

- [ ] Added policy snapshot capture to pipeline startup
- [ ] Tested with sample run
- [ ] Verified snapshot file created in .runs/

### Step 13: Test Historical Query
```bash
# Query policies for a specific run
python examples/example_integration.py query <run_id>
```

- [ ] Queried historical run
- [ ] Retrieved policy versions correctly

## Phase 5: Team Training (30 minutes)

### Step 14: Create Documentation
- [ ] Share `AUTOMATED_DOCS_GUIDE.md` with team
- [ ] Walk through example PR workflow
- [ ] Demonstrate error messages

### Step 15: Practice Workflow
Have team members practice:
1. Creating branch
2. Editing document
3. Bumping version
4. Creating PR with conventional commit
5. Handling CI feedback

- [ ] Team member 1 completed practice ✅
- [ ] Team member 2 completed practice ✅
- [ ] Team member 3 completed practice ✅

## Phase 6: Verification (15 minutes)

### Step 16: End-to-End Test
```bash
# Complete workflow test
git checkout -b test/full-workflow

# 1. Edit document (bump version)
# 2. Commit with conventional format
# 3. Create PR
# 4. Wait for CI validation
# 5. Get approval
# 6. Merge
# 7. Verify tag created
# 8. Run pipeline
# 9. Check policy snapshot
```

- [ ] One-document rule enforced
- [ ] Front-matter validated
- [ ] SemVer bump validated
- [ ] PR title checked
- [ ] Uniqueness verified
- [ ] Tag auto-created
- [ ] Policy snapshot captured

### Step 17: Rollback Test
```bash
# Test that you can checkout old versions
git tag -l "docs-*" | head -1  # Get first tag
git checkout <tag-name>
cat docs/path/to/doc.md  # Should show old version
git checkout main  # Return to current
```

- [ ] Can checkout historical versions
- [ ] Content matches expected version
- [ ] Can return to current state

## Success Criteria

Your system is working correctly when:

- ✅ CI blocks PRs with multiple documents changed
- ✅ CI blocks PRs with invalid front-matter
- ✅ CI blocks PRs with incorrect version bumps
- ✅ CI blocks PRs with duplicate doc_keys
- ✅ Tags are auto-created after merge
- ✅ Policy snapshots captured on pipeline runs
- ✅ Historical queries work correctly

## Common Issues & Solutions

### Issue: CI not triggering
**Solution:** Check that workflows are in `.github/workflows/` and merged to main

### Issue: Tag not created
**Solution:** Check workflow permissions in Settings → Actions → General → Workflow permissions

### Issue: Registry shows duplicates
**Solution:** Each doc_key must be unique - rename one of the conflicting documents

### Issue: SemVer validation fails
**Solution:** Ensure version increased from previous version

## Rollback Plan

If something goes wrong:

```bash
# 1. Disable branch protection temporarily
# 2. Revert the setup commits
git revert <commit-hash>

# 3. Remove workflows
rm .github/workflows/docs-guard.yml
rm .github/workflows/doc-tags.yml

# 4. Commit and push
git commit -m "revert: Remove docs automation (temporary)"
git push

# 5. Fix issues
# 6. Re-enable by following checklist again
```

## Notes

- Date completed: _________________
- Completed by: _________________
- Issues encountered: _________________
- Additional notes: _________________

---

## Quick Reference

**Start a document update:**
```bash
git checkout -b docs/DOCNAME/description
# Edit ONE document, bump version
git commit -m "fix|feat|feat!: Description"
git push
```

**Check CI status:**
```bash
gh pr checks
```

**View tags:**
```bash
git tag -l "docs-*"
```

**Checkout old version:**
```bash
git checkout docs-DOCNAME-X.Y.Z
```

**Query run policies:**
```bash
python examples/example_integration.py query <run_id>
```
