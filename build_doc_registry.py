#!/usr/bin/env python3
"""
Document Registry Builder

Scans all markdown files in docs/ and plans/ directories, extracts front-matter,
and builds a registry ensuring doc_key uniqueness. This is the foundation for
the automated documentation management system.

Usage:
    python scripts/build_doc_registry.py
    python scripts/build_doc_registry.py --check-only
    python scripts/build_doc_registry.py --output custom_registry.json
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
import argparse


@dataclass
class DocumentRecord:
    """Single document entry in the registry"""
    doc_key: str
    path: str
    semver: str
    status: str
    effective_date: str
    owner: str
    contract_type: str
    supersedes_version: Optional[str] = None


class DocRegistryBuilder:
    """Builds and validates document registry"""
    
    def __init__(self, repo_root: Path = Path(".")):
        self.repo_root = repo_root
        self.registry: Dict[str, DocumentRecord] = {}
        self.duplicates: List[Tuple[str, str, str]] = []
        self.errors: List[str] = []
        
    def extract_frontmatter(self, file_path: Path) -> Optional[Dict]:
        """
        Extract YAML front-matter from markdown file.
        
        Returns:
            Dict of front-matter fields, or None if no valid front-matter
        """
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            self.errors.append(f"Cannot read {file_path}: {e}")
            return None
        
        # Check for YAML front-matter delimiters
        if not content.startswith('---'):
            return None
        
        # Extract content between first two '---' markers
        parts = content.split('---', 2)
        if len(parts) < 3:
            return None
        
        frontmatter_text = parts[1].strip()
        
        # Parse YAML manually (avoid external dependency)
        metadata = {}
        for line in frontmatter_text.split('\n'):
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                # Handle quoted strings
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                
                # Handle null values
                if value.lower() in ('null', '~', ''):
                    value = None
                
                metadata[key] = value
        
        return metadata if metadata else None
    
    def validate_frontmatter(self, metadata: Dict, file_path: Path) -> bool:
        """
        Validate that required front-matter fields are present.
        
        Required fields per VERSIONING_OPERATING_CONTRACT:
        - doc_key
        - semver
        - status
        - effective_date
        - owner
        - contract_type
        """
        required_fields = [
            'doc_key', 'semver', 'status', 
            'effective_date', 'owner', 'contract_type'
        ]
        
        missing = [f for f in required_fields if f not in metadata]
        
        if missing:
            self.errors.append(
                f"{file_path}: Missing required fields: {', '.join(missing)}"
            )
            return False
        
        # Validate semver format (MAJOR.MINOR.PATCH)
        semver_pattern = r'^\d+\.\d+\.\d+$'
        if not re.match(semver_pattern, str(metadata['semver'])):
            self.errors.append(
                f"{file_path}: Invalid semver format '{metadata['semver']}' "
                f"(must be MAJOR.MINOR.PATCH)"
            )
            return False
        
        # Validate status enum
        valid_statuses = ['active', 'deprecated', 'frozen']
        if metadata['status'] not in valid_statuses:
            self.errors.append(
                f"{file_path}: Invalid status '{metadata['status']}' "
                f"(must be one of: {', '.join(valid_statuses)})"
            )
            return False
        
        # Validate contract_type enum
        valid_types = ['policy', 'intent', 'execution_contract']
        if metadata['contract_type'] not in valid_types:
            self.errors.append(
                f"{file_path}: Invalid contract_type '{metadata['contract_type']}' "
                f"(must be one of: {', '.join(valid_types)})"
            )
            return False
        
        return True
    
    def scan_documents(self) -> int:
        """
        Scan docs/ and plans/ directories for versioned documents.
        
        Returns:
            Number of valid documents found
        """
        search_roots = [
            self.repo_root / "docs",
            self.repo_root / "plans"
        ]
        
        doc_count = 0
        
        for root in search_roots:
            if not root.exists():
                continue
            
            for md_file in root.rglob("*.md"):
                # Extract front-matter
                metadata = self.extract_frontmatter(md_file)
                if not metadata:
                    continue
                
                # Skip if no doc_key (not a versioned document)
                if 'doc_key' not in metadata:
                    continue
                
                # Validate front-matter
                if not self.validate_frontmatter(metadata, md_file):
                    continue
                
                doc_key = metadata['doc_key']
                
                # Check for duplicates
                if doc_key in self.registry:
                    existing_path = self.registry[doc_key].path
                    self.duplicates.append((
                        doc_key,
                        existing_path,
                        str(md_file.relative_to(self.repo_root))
                    ))
                else:
                    # Add to registry
                    self.registry[doc_key] = DocumentRecord(
                        doc_key=doc_key,
                        path=str(md_file.relative_to(self.repo_root)),
                        semver=metadata['semver'],
                        status=metadata['status'],
                        effective_date=metadata['effective_date'],
                        owner=metadata['owner'],
                        contract_type=metadata['contract_type'],
                        supersedes_version=metadata.get('supersedes_version')
                    )
                    doc_count += 1
        
        return doc_count
    
    def save_registry(self, output_path: Path):
        """Save registry to JSON file"""
        # Convert to dict format
        registry_dict = {
            doc_key: asdict(record)
            for doc_key, record in self.registry.items()
        }
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(registry_dict, f, indent=2, sort_keys=True)
    
    def report_status(self) -> bool:
        """
        Print status report and return success/failure.
        
        Returns:
            True if no errors or duplicates, False otherwise
        """
        print(f"✓ Found {len(self.registry)} versioned documents")
        
        if self.duplicates:
            print("\n❌ DUPLICATE doc_key DETECTED:")
            for doc_key, path1, path2 in self.duplicates:
                print(f"  • {doc_key}:")
                print(f"    - {path1}")
                print(f"    - {path2}")
            print("\nEach document must have a unique doc_key identifier.")
            return False
        
        if self.errors:
            print("\n❌ VALIDATION ERRORS:")
            for error in self.errors:
                print(f"  • {error}")
            return False
        
        print("✓ All doc_key identifiers are unique")
        print("✓ All front-matter is valid")
        return True


def main():
    parser = argparse.ArgumentParser(
        description="Build document registry and enforce unique doc_key identifiers"
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('.runs/doc-registry.json'),
        help='Output path for registry JSON (default: .runs/doc-registry.json)'
    )
    parser.add_argument(
        '--check-only',
        action='store_true',
        help='Only validate, do not write registry file'
    )
    parser.add_argument(
        '--repo-root',
        type=Path,
        default=Path('.'),
        help='Repository root directory (default: current directory)'
    )
    
    args = parser.parse_args()
    
    # Build registry
    builder = DocRegistryBuilder(repo_root=args.repo_root)
    doc_count = builder.scan_documents()
    
    # Report status
    success = builder.report_status()
    
    # Save registry (unless check-only mode)
    if success and not args.check_only:
        builder.save_registry(args.output)
        print(f"✓ Registry saved to {args.output}")
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
