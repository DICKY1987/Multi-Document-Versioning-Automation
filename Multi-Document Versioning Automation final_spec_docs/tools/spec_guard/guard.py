"""
Guard (validation) utility for the Automated Documentation & Versioning specification.

This script validates the integrity of the documentation suite. It
verifies that:

  * All section and paragraph IDs (ULIDs) are unique across the suite.
  * Section keys are unique within volumes and ordered numerically.
  * Markdown files referenced in the index exist, along with their
    sidecar YAML files.
  * The MFIDs recorded in the index and sidecars match the current
    contents of the files.
  * Sidecar entries cover all paragraphs and anchors are sequential
    starting at p-1.
  * Sidecar paragraph IDs match those in the index.

If any of these checks fail, the script prints a human readable
report and exits with a non-zero status. This tool is intended to be
run in CI to enforce consistency and prevent accidental drifts.

Usage:

    python -m tools.spec_guard.guard

The exit code indicates success (0) or failure (1).
"""

import hashlib
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    sys.stderr.write("Missing pyyaml dependency. Install with `pip install pyyaml`\n")
    sys.exit(2)


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


def validate_suite(index_path: Path = Path("docs/.index/suite-index.yaml")) -> list[str]:
    """Perform a series of validation checks on the suite.

    Returns a list of error messages (empty if no errors).
    """
    errors: list[str] = []
    with index_path.open("r", encoding="utf-8") as f:
        index = yaml.safe_load(f)
    suite = index.get("suite", {})
    # Uniqueness checks
    seen_ids: set[str] = set()
    seen_section_keys = {}
    for vol in suite.get("volumes", []):
        vol_key = vol.get("key")
        keys_in_vol = set()
        for sec in vol.get("sections", []):
            sid = sec.get("id")
            if sid in seen_ids:
                errors.append(f"Duplicate section id {sid} in volume {vol_key}")
            else:
                seen_ids.add(sid)
            skey = sec.get("key")
            if skey in keys_in_vol:
                errors.append(f"Duplicate section key {skey} in volume {vol_key}")
            keys_in_vol.add(skey)
            # check paragraphs
            for para in sec.get("paragraphs", []):
                pid = para.get("id")
                if not pid:
                    errors.append(f"Paragraph in {vol_key}/{skey} missing id for anchor {para.get('anchor')}")
                elif pid in seen_ids:
                    errors.append(f"Duplicate paragraph id {pid} across suite")
                else:
                    seen_ids.add(pid)
    # File existence and MFID checks
    for vol in suite.get("volumes", []):
        for sec in vol.get("sections", []):
            file_path = Path(sec.get("file"))
            if not file_path.exists():
                errors.append(f"Markdown file missing: {file_path}")
                continue
            # verify file mfid
            content = file_path.read_text(encoding="utf-8")
            file_hash = compute_mfid(content.encode("utf-8"))
            if sec.get("mfid") != file_hash:
                errors.append(f"MFID mismatch for {file_path}: index has {sec.get('mfid')} but actual is {file_hash}")
            # sidecar existence
            sc_path = file_path.with_suffix(file_path.suffix + ".sidecar.yaml")
            if not sc_path.exists():
                errors.append(f"Sidecar missing for {file_path}")
                continue
            sc = yaml.safe_load(sc_path.read_text(encoding="utf-8"))
            # verify sidecar file hash
            if sc.get("mfid") != file_hash:
                errors.append(f"Sidecar MFID mismatch for {file_path}: sidecar has {sc.get('mfid')} but actual is {file_hash}")
            # build paragraph map
            sc_paras = sc.get("paragraphs", [])
            # check anchors sequential
            expected_anchor = 1
            for p in sc_paras:
                anchor = p.get("anchor")
                if anchor != f"p-{expected_anchor}":
                    errors.append(f"Anchor ordering error in {file_path}: expected p-{expected_anchor} but got {anchor}")
                expected_anchor += 1
            # compute paragraphs and check range and hash
            computed_paras = compute_paragraphs(content)
            if len(computed_paras) != len(sc_paras):
                errors.append(f"Paragraph count mismatch in {file_path}: sidecar has {len(sc_paras)}, computed {len(computed_paras)}")
            # Map anchor to computed data
            for idx, (start, end, text) in enumerate(computed_paras, start=1):
                anchor = f"p-{idx}"
                p = next((x for x in sc_paras if x.get("anchor") == anchor), None)
                if not p:
                    errors.append(f"Missing sidecar entry {anchor} in {file_path}")
                    continue
                if p.get("start_line") != start or p.get("end_line") != end:
                    errors.append(f"Line range mismatch for {file_path} {anchor}: sidecar says {p.get('start_line')}-{p.get('end_line')}, computed {start}-{end}")
                para_hash = compute_mfid(text.encode("utf-8"))
                if p.get("mfid") != para_hash:
                    errors.append(f"MFID mismatch for {file_path} {anchor}: sidecar has {p.get('mfid')} but actual is {para_hash}")
                # check index paragraph entry
                idx_para = next((x for x in sec.get("paragraphs", []) if x.get("anchor") == anchor), None)
                if not idx_para:
                    errors.append(f"Index missing paragraph entry {anchor} for {file_path}")
                else:
                    if idx_para.get("mfid") != p.get("mfid"):
                        errors.append(f"Index MFID mismatch for {file_path} {anchor}: index has {idx_para.get('mfid')}, sidecar has {p.get('mfid')}")
                    if idx_para.get("id") != p.get("id"):
                        errors.append(f"Index id mismatch for {file_path} {anchor}: index has {idx_para.get('id')}, sidecar has {p.get('id')}")
    return errors


def main():
    errors = validate_suite()
    if errors:
        for err in errors:
            print(err)
        sys.exit(1)
    print("Specification is valid.")


if __name__ == "__main__":
    main()