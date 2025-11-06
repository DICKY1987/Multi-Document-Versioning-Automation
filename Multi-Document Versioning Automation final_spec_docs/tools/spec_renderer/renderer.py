"""
Renderer for the Automated Documentation & Versioning specification.

This script stitches the split documentation suite into a single
readable Markdown file. It walks the suite index in order,
concatenating the contents of each section according to the
architecture defined in `docs/.index/suite-index.yaml`.

By default the renderer outputs the combined document to stdout, but
the result can be saved to a file with the `--output` flag.

Usage:

    python -m tools.spec_renderer.renderer > build/spec.md

This tool does not modify any source files. It simply reads the
existing Markdown files and their order from the index. Headings are
included to denote volumes and sections.
"""

import argparse
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    sys.stderr.write("Missing pyyaml dependency. Install with `pip install pyyaml`\n")
    sys.exit(2)


def load_suite_index(path: str = "docs/.index/suite-index.yaml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def render_spec(index: dict) -> str:
    """Render the entire specification into a single Markdown string."""
    lines = []
    # document title
    suite = index.get("suite", {})
    title = suite.get("title", "Specification")
    lines.append(f"# {title}\n")
    # Optionally include version/date
    version = suite.get("version")
    eff_date = suite.get("effective_date")
    meta = []
    if version:
        meta.append(f"Version {version}")
    if eff_date:
        meta.append(f"Effective {eff_date}")
    if meta:
        lines.append(f"_({', '.join(meta)})_\n\n")
    for vol in suite.get("volumes", []):
        vol_title = vol.get("title")
        vol_key = vol.get("key")
        lines.append(f"\n## {vol_key} {vol_title}\n")
        for section in vol.get("sections", []):
            sec_title = section.get("title")
            sec_key = section.get("key")
            lines.append(f"\n### {vol_key}/{sec_key} {sec_title}\n")
            # Append the raw contents of the file
            content = read_file(section["file"])
            lines.append(content.rstrip() + "\n")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Render the split specification into a single Markdown file")
    parser.add_argument("--output", "-o", help="Path to write the rendered markdown. Defaults to stdout")
    args = parser.parse_args()
    index = load_suite_index()
    output = render_spec(index)
    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(output)
    else:
        sys.stdout.write(output)


if __name__ == "__main__":
    main()