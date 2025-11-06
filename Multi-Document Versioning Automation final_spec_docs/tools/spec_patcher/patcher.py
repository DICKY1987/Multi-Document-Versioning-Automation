"""
Patcher utility for the Automated Documentation & Versioning specification.

This script applies precise edits to a specification document given a
globally unique paragraph identifier (specid). It replaces the content
of the identified paragraph with new text, then updates the
corresponding sidecar and suite index entries. This enables
fine‑grained modifications without manually editing the Markdown
files or the index.

Usage:

    python -m tools.spec_patcher.patcher --id <ULID> --file replacement.md

The replacement can be provided either via --text for inline
replacement or via --file to load the replacement content from a
Markdown file. The replacement content will completely replace the
original paragraph lines.

After the replacement, the script recalculates the MFIDs for the
modified file and its paragraphs, updates the sidecar, and rewrites
the suite index with the new hashes. Paragraph IDs are preserved.

NOTE: This tool performs immediate updates. It is advised to run
`tools/spec-guard/guard.py` after patching to verify overall
consistency.
"""

import argparse
import hashlib
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    print("Missing pyyaml dependency. Install with `pip install pyyaml`.", file=sys.stderr)
    sys.exit(2)


def compute_mfid(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compute_paragraphs(text: str):
    """Split text into (start_line, end_line, paragraph_text) tuples.

    Paragraphs are sequences of non-blank lines separated by one or more
    blank lines. Leading and trailing whitespace is preserved in the
    paragraph hash.
    """
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


def load_suite_index(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_suite_index(data: dict, path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False)


def load_sidecar(md_path: Path) -> dict:
    sc_path = md_path.with_suffix(md_path.suffix + ".sidecar.yaml")
    with sc_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_sidecar(sc: dict, md_path: Path) -> None:
    sc_path = md_path.with_suffix(md_path.suffix + ".sidecar.yaml")
    with sc_path.open("w", encoding="utf-8") as f:
        yaml.dump(sc, f, sort_keys=False)


def replace_paragraph(md_path: Path, start_line: int, end_line: int, replacement_lines: list[str]) -> None:
    """Replace lines [start_line, end_line] (1-indexed) in the file with replacement_lines."""
    with md_path.open("r", encoding="utf-8") as f:
        lines = f.read().splitlines(keepends=True)
    # adjust index: convert to 0-based indices
    start_idx = start_line - 1
    end_idx = end_line - 1
    new_lines = lines[:start_idx] + [line + "\n" for line in replacement_lines] + lines[end_idx + 1:]
    with md_path.open("w", encoding="utf-8") as f:
        f.writelines(new_lines)


def main():
    parser = argparse.ArgumentParser(description="Patch a specification paragraph by id")
    parser.add_argument("--id", required=True, help="ULID of the paragraph to replace")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="Inline replacement text")
    group.add_argument("--file", help="Path to a file containing replacement text")
    args = parser.parse_args()

    spec_id = args.id
    replacement_text: str
    if args.text is not None:
        replacement_text = args.text
    else:
        rep_path = Path(args.file)
        if not rep_path.exists():
            parser.error(f"Replacement file {rep_path} does not exist")
        replacement_text = rep_path.read_text(encoding="utf-8")

    # load index
    index_path = Path("docs/.index/suite-index.yaml")
    index_data = load_suite_index(index_path)
    suite = index_data.get("suite", {})
    # find paragraph in index
    found = None
    for vol in suite.get("volumes", []):
        for sec in vol.get("sections", []):
            for para in sec.get("paragraphs", []):
                if para.get("id") == spec_id:
                    found = (vol, sec, para)
                    break
            if found:
                break
        if found:
            break
    if not found:
        print(f"Paragraph id {spec_id} not found in index", file=sys.stderr)
        sys.exit(1)
    vol, sec, para = found
    md_path = Path(sec["file"])
    # load sidecar to get line range
    sc = load_sidecar(md_path)
    p_entry = None
    for p in sc.get("paragraphs", []):
        if p.get("id") == spec_id:
            p_entry = p
            break
    if not p_entry:
        print(f"Paragraph id {spec_id} not found in sidecar", file=sys.stderr)
        sys.exit(1)
    start_line = p_entry["start_line"]
    end_line = p_entry["end_line"]
    # replace lines in file
    replacement_lines = replacement_text.splitlines()
    replace_paragraph(md_path, start_line, end_line, replacement_lines)
    # re-read file and recompute paragraphs
    updated_text = md_path.read_text(encoding="utf-8")
    paragraphs = compute_paragraphs(updated_text)
    # update sidecar paragraphs: preserve ids based on anchor & old IDs mapping
    old_entries = { (p['anchor'], p['start_line'], p['end_line']): p['id'] for p in sc.get('paragraphs', []) }
    new_p_entries = []
    for idx, (start, end, para_text) in enumerate(paragraphs, start=1):
        anchor = f"p-{idx}"
        # find id: match by anchor and line range, else reuse by anchor only
        pid = None
        # try to match start and end lines
        pid = old_entries.get((anchor, start, end))
        # fallback: search old paragraphs with same anchor
        if pid is None:
            for key, val in old_entries.items():
                if key[0] == anchor:
                    pid = val
                    break
        p_hash = compute_mfid(para_text.encode("utf-8"))
        new_p_entries.append({
            "anchor": anchor,
            "start_line": start,
            "end_line": end,
            "mfid": p_hash,
            "id": pid or p_entry["id"] if anchor == p_entry["anchor"] else "",
        })
    # update sidecar file hash
    file_hash = compute_mfid(updated_text.encode("utf-8"))
    new_sc = {
        "file": str(md_path),
        "mfid": file_hash,
        "paragraphs": new_p_entries,
    }
    save_sidecar(new_sc, md_path)
    # update index entry
    sec["mfid"] = file_hash
    # rebuild paragraphs list with new hashes preserving ids
    index_paras = []
    for p in new_p_entries:
        # ensure id present
        pid = p["id"]
        if not pid:
            # generate a new id (could generate ULID but leave blank)
            pid = para["id"]
        index_paras.append({
            "id": pid,
            "anchor": p["anchor"],
            "mfid": p["mfid"],
        })
    sec["paragraphs"] = index_paras
    # write back index
    save_suite_index(index_data, index_path)
    print(f"Patched paragraph {spec_id} in {md_path}, updated sidecar and index.")


if __name__ == "__main__":
    main()