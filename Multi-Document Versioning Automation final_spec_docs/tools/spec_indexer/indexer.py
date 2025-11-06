"""
Indexer utility for the Automated Documentation & Versioning specification.

This script scans all Markdown files under a given directory (by
default `docs/source`) and produces a sidecar YAML for each file.
The sidecar contains:

  * The MFID (SHA‑256 hash) of the entire file
  * A list of paragraphs with their anchor (p-1, p-2, ...), line
    range and MFID
  * Paragraph IDs are preserved if already present in an existing
    sidecar; otherwise they are left blank for the index to populate.

Usage:

    python -m tools.spec_indexer.indexer [root]

Running this tool before committing changes helps ensure sidecar files
remain in sync with the Markdown content.
"""

import os
import hashlib
import yaml


def compute_mfid(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compute_paragraphs(text: str):
    paragraphs = []
    lines = text.splitlines()
    start = None
    buffer = []
    for i, line in enumerate(lines, start=1):
        if not line.strip():
            if start is not None:
                paragraphs.append((start, i - 1, "\n".join(buffer)))
                start = None
                buffer = []
            continue
        if start is None:
            start = i
        buffer.append(line)
    if start is not None:
        paragraphs.append((start, len(lines), "\n".join(buffer)))
    return paragraphs


def generate_sidecar(md_path: str):
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()
    file_hash = compute_mfid(content.encode("utf-8"))
    paragraphs = compute_paragraphs(content)
    sidecar_path = md_path + ".sidecar.yaml"
    existing = {}
    if os.path.exists(sidecar_path):
        with open(sidecar_path, "r", encoding="utf-8") as f:
            try:
                data = yaml.safe_load(f) or {}
                for p in data.get("paragraphs", []):
                    key = (p.get("anchor"), p.get("start_line"), p.get("end_line"))
                    existing[key] = p.get("id")
            except yaml.YAMLError:
                pass
    entries = []
    for idx, (start, end, text) in enumerate(paragraphs, start=1):
        anchor = f"p-{idx}"
        mfid = compute_mfid(text.encode("utf-8"))
        pid = existing.get((anchor, start, end)) or ""
        entries.append({
            "anchor": anchor,
            "start_line": start,
            "end_line": end,
            "mfid": mfid,
            "id": pid,
        })
    sidecar = {
        "file": md_path,
        "mfid": file_hash,
        "paragraphs": entries,
    }
    with open(sidecar_path, "w", encoding="utf-8") as f:
        yaml.dump(sidecar, f, sort_keys=False)
    return sidecar


def main(root: str = "docs/source"):
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            if name.endswith(".md"):
                path = os.path.join(dirpath, name)
                print(f"Processing {path}")
                generate_sidecar(path)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()