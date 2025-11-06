"""
Resolver tool for the Automated Documentation & Versioning specification.

This script resolves spec addresses to their underlying file locations and
paragraph spans. It supports two addressing formats:

  • spec://VOLUME/SECTION[.SUBSECTION][#ANCHOR]
      Resolves to the given volume key, section key and optional paragraph
      anchor (e.g. p-3). If an anchor is not supplied the entire section
      file is returned.

  • specid://<ULID>
      Resolves a globally unique identifier (ULID) assigned to a section
      or paragraph. This returns the file path and line range for that
      object.

Example usage:

    python -m tools.spec_resolver.resolver spec://ARCH/1.1#p-2
    python -m tools.spec_resolver.resolver specid://XY123...

The output is a simple JSON structure describing the resolved location.

Note: this tool does not perform any modifications. It relies on the
suite index (`docs/.index/suite-index.yaml`) and sidecar files to
resolve anchors.
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    print("Missing pyyaml dependency. Install with `pip install pyyaml`.", file=sys.stderr)
    sys.exit(2)


def load_suite_index(path: str = "docs/.index/suite-index.yaml") -> dict:
    """Load and return the suite index YAML as a Python dictionary."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_sidecar(path: str) -> dict:
    """Load a sidecar YAML given a markdown file path."""
    sidecar_path = path + ".sidecar.yaml"
    with open(sidecar_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def resolve_spec_uri(uri: str, index: dict) -> dict:
    """Resolve a spec://... or specid://... URI into a concrete location.

    Returns a dict with keys:
      * type: 'section' or 'paragraph'
      * id: ULID of the matched object
      * file: path to the markdown file
      * start_line, end_line: line numbers (for paragraphs)
      * anchor: paragraph anchor if applicable
      * volume_key, section_key: identifiers for the containing objects
      * title: human‑readable title of the section
    """
    if uri.startswith("specid://"):
        target_id = uri[len("specid://"):]
        for volume in index.get("suite", {}).get("volumes", []):
            for section in volume.get("sections", []):
                # Check if section matches
                if section.get("id") == target_id:
                    return {
                        "type": "section",
                        "id": section["id"],
                        "file": section["file"],
                        "volume_key": volume["key"],
                        "section_key": section["key"],
                        "title": section["title"],
                    }
                # Check paragraphs
                for para in section.get("paragraphs", []):
                    if para.get("id") == target_id:
                        # load sidecar to get line numbers
                        sc = load_sidecar(section["file"])
                        # match by id
                        for p in sc.get("paragraphs", []):
                            if p.get("id") == target_id:
                                return {
                                    "type": "paragraph",
                                    "id": para["id"],
                                    "file": section["file"],
                                    "start_line": p.get("start_line"),
                                    "end_line": p.get("end_line"),
                                    "anchor": p.get("anchor"),
                                    "volume_key": volume["key"],
                                    "section_key": section["key"],
                                    "title": section["title"],
                                }
        raise KeyError(f"No object found with id {target_id}")

    if uri.startswith("spec://"):
        # spec://VOL/SECTION[.SUBSECTION][#ANCHOR]
        body = uri[len("spec://"):]
        anchor = None
        if "#" in body:
            body, anchor = body.split("#", 1)
        parts = body.split("/", 1)
        if len(parts) != 2:
            raise ValueError("Invalid spec:// URI; expected spec://VOLUME/SECTION")
        vol_key, sec_key = parts
        # locate volume
        for volume in index.get("suite", {}).get("volumes", []):
            if volume.get("key") == vol_key:
                for section in volume.get("sections", []):
                    if section.get("key") == sec_key:
                        if anchor is None:
                            return {
                                "type": "section",
                                "id": section["id"],
                                "file": section["file"],
                                "volume_key": volume["key"],
                                "section_key": section["key"],
                                "title": section["title"],
                            }
                        # anchor specified; find paragraph by anchor
                        sc = load_sidecar(section["file"])
                        for p in sc.get("paragraphs", []):
                            if p.get("anchor") == anchor:
                                return {
                                    "type": "paragraph",
                                    "id": p.get("id"),
                                    "file": section["file"],
                                    "start_line": p.get("start_line"),
                                    "end_line": p.get("end_line"),
                                    "anchor": p.get("anchor"),
                                    "volume_key": volume["key"],
                                    "section_key": section["key"],
                                    "title": section["title"],
                                }
                        raise KeyError(f"Anchor {anchor} not found in section {sec_key}")
        raise KeyError(f"No matching section {sec_key} in volume {vol_key}")

    raise ValueError("Unsupported URI scheme; use spec:// or specid://")


def main():
    parser = argparse.ArgumentParser(description="Resolve specification URIs to file locations")
    parser.add_argument("uri", help="spec:// or specid:// URI to resolve")
    args = parser.parse_args()
    index = load_suite_index()
    try:
        result = resolve_spec_uri(args.uri, index)
    except Exception as exc:
        print(json.dumps({"error": str(exc)}))
        sys.exit(1)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()