# Lifecycle & Identity Extensions

## Consolidation/Merge

When documents are consolidated, the target retains its ULID and the sources become immutable with a `merged_into` field pointing to the target.  The target may declare an `absorbs` array listing the source ULIDs.  A **CONSOLIDATE** event records the merge.

## MFID Update

Any content change that updates the `mfid` triggers an **MFID_UPDATE** event.  If the MFID changes without a SemVer bump, CI fails; semantic versioning must reflect meaningful content changes.
