#!/usr/bin/env python
"""
Capture the policy snapshot at runtime (issue 15).

This script serializes the active policy artefacts (e.g. the
consolidated policy snapshot from `policy_snapshot.json`, local
overrides, retention rules) into a JSON object and writes it to
`.runs/<RUN_ID>/policies.json`. The snapshot may then be included
in runtime artefacts such as run ledgers to ensure reproducibility.
"""

import json
import os
from pathlib import Path
from datetime import datetime

def capture_snapshot(run_id):
    base = Path(__file__).resolve().parents[1]
    policies = {}
    for policy_file in (base / 'policy').glob('*.yml'):
        policies[policy_file.name] = policy_file.read_text(encoding='utf-8')
    snapshot = {
        'run_id': run_id,
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'policies': policies
    }
    out_dir = base / '.runs' / run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / 'policies.json'
    out_path.write_text(json.dumps(snapshot, indent=2), encoding='utf-8')
    print(f"Snapshot written to {out_path}")

if __name__ == '__main__':
    run_id = os.environ.get('GITHUB_RUN_ID', 'local')
    capture_snapshot(run_id)