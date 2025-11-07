#!/usr/bin/env python
"""
generate_plugin_files.py (issue 21)

This script reads a `plugin.spec.json` file and generates the
derived artefacts: `manifest.json`, per-op input/output schemas,
and test skeletons. It demonstrates how a fully autonomous release
process might materialize plugin definitions from a single source
of truth. In a real implementation, extend this script to cover
all fields defined in your contract specification.
"""

import json
import os
from pathlib import Path
from datetime import datetime

def generate_manifest(spec_path: Path):
    spec = json.loads(spec_path.read_text(encoding='utf-8'))
    manifest = {
        "key": spec["key"],
        "name": spec["name"],
        "version": spec["version"],
        "manifest_schema_version": "1.0.0",
        "build": {
            "built_at": datetime.utcnow().isoformat() + 'Z',
            "spec_hash": "TODO",
        },
        "runtime": {
            "language": "python",
        },
        "entrypoints": {
            "handlers": []
        },
        "compatibility": spec.get("contract", {}),
        "permissions": spec.get("actions", {}),
        "config": {
            "schema_ref": spec.get("config", {}).get("schema", ""),
            "defaults": spec.get("config", {}).get("defaults", {})
        }
    }
    return manifest

def main():
    for spec_file in Path("plugins").rglob("plugin.spec.json"):
        manifest = generate_manifest(spec_file)
        manifest_path = spec_file.parent / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
        print(f"Generated {manifest_path}")

if __name__ == '__main__':
    main()