# New Plugins

## docs.migrate

**Purpose**: Bootstrap legacy Markdown into governed Cards and the Registry.

**Inputs**: roots, default owner/team, key strategy (`slug` or `map`), collision policy (`skip|overwrite|fail`).

**Behavior**:
1. Discover docs lacking ULID.
2. Mint ULIDs and Cards; write `CREATE` events.
3. Generate/refresh the registry; print a migration report.

**Acceptance**: All discovered docs yield valid Cards; the registry has no orphans; the ledger records a `CREATE` event per new card.

## id.mfid.update

**Purpose**: Compute the canonical MFID for a doc and store it in the Card; append an `MFID_UPDATE` event.

**Normalization**: Convert line endings to LF and trim trailing whitespace; preserve UTF‑8.
