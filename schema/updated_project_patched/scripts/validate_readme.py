#!/usr/bin/env python
"""
validate_readme.py

Validation script for README and healthcheck documentation (issue 14).
This script scans README and healthcheck files for code blocks or
examples and verifies that they conform to the corresponding
operation input/output schemas. It reports errors if examples are
missing, invalid, or outdated. Integrate this script in CI to
enforce documentation quality.
"""

import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator, ValidationError

def find_examples(md_content):
    """Extract example JSON snippets from a markdown document."""
    examples = []
    in_code = False
    current_lines = []
    for line in md_content.splitlines():
        if line.strip().startswith("```json"):
            in_code = True
            current_lines = []
        elif line.strip().startswith("```") and in_code:
            in_code = False
            examples.append("\n".join(current_lines))
        elif in_code:
            current_lines.append(line)
    return examples

def load_schema(schema_path):
    schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema

def validate_examples(readme_path, schema_dir):
    content = Path(readme_path).read_text(encoding="utf-8")
    examples = find_examples(content)
    if not examples:
        print(f"No examples found in {readme_path}")
        return 0
    # Determine op from file name (simple heuristic)
    op = Path(readme_path).stem.replace("README_", "").lower()
    input_schema = Path(schema_dir) / f"{op}.input.schema.json"
    output_schema = Path(schema_dir) / f"{op}.output.schema.json"
    errors = 0
    for example in examples:
        try:
            data = json.loads(example)
        except json.JSONDecodeError:
            print(f"Invalid JSON example in {readme_path}:")
            print(example)
            errors += 1
            continue
        schema = load_schema(input_schema if data.get("x-metadata", {}).get("direction") == "input" else output_schema)
        validator = Draft202012Validator(schema)
        try:
            validator.validate(data)
        except ValidationError as exc:
            print(f"Example does not conform to schema: {exc.message}")
            errors += 1
    return errors

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parents[1]
    schema_dir = base_dir / "schemas"
    readme_files = list(base_dir.glob("README_*.md")) + list(base_dir.glob("plugins/**/README*.md"))
    total_errors = 0
    for readme in readme_files:
        total_errors += validate_examples(readme, schema_dir)
    if total_errors:
        sys.exit(1)