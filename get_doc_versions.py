#!/usr/bin/env python3
"""
Get Active Document Versions

Extracts current versions of all active documents for runtime logging.
This ensures every pipeline run records which policy/contract versions
were in force during execution.

Usage:
    python scripts/get_doc_versions.py
    python scripts/get_doc_versions.py --format json
    python scripts/get_doc_versions.py --output versions.json
    python scripts/get_doc_versions.py --status active
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import argparse


@dataclass
class DocumentVersion:
    """Document version information"""
    doc_key: str
    semver: str
    status: str
    effective_date: str
    contract_type: str
    path: str


class DocumentVersionExtractor:
    """Extract current versions of all documents"""
    
    def __init__(self, repo_root: Path = Path(".")):
        self.repo_root = repo_root
        self.versions: Dict[str, DocumentVersion] = {}
    
    def extract_frontmatter(self, file_path: Path) -> Optional[Dict]:
        """Extract YAML front-matter from markdown file"""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception:
            return None
        
        if not content.startswith('---'):
            return None
        
        parts = content.split('---', 2)
        if len(parts) < 3:
            return None
        
        metadata = {}
        for line in parts[1].strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if value.lower() in ('null', '~', ''):
                    value = None
                metadata[key] = value
        
        return metadata if metadata else None
    
    def scan_documents(self, status_filter: Optional[str] = None) -> int:
        """
        Scan repository for versioned documents
        
        Args:
            status_filter: Only include documents with this status (e.g., 'active')
        
        Returns:
            Number of documents found
        """
        search_roots = [
            self.repo_root / "docs",
            self.repo_root / "plans"
        ]
        
        count = 0
        
        for root in search_roots:
            if not root.exists():
                continue
            
            for md_file in root.rglob("*.md"):
                metadata = self.extract_frontmatter(md_file)
                if not metadata or 'doc_key' not in metadata:
                    continue
                
                # Apply status filter if specified
                if status_filter and metadata.get('status') != status_filter:
                    continue
                
                # Require minimum fields
                required = ['doc_key', 'semver', 'status', 'effective_date', 'contract_type']
                if not all(f in metadata for f in required):
                    continue
                
                doc_key = metadata['doc_key']
                
                self.versions[doc_key] = DocumentVersion(
                    doc_key=doc_key,
                    semver=metadata['semver'],
                    status=metadata['status'],
                    effective_date=metadata['effective_date'],
                    contract_type=metadata['contract_type'],
                    path=str(md_file.relative_to(self.repo_root))
                )
                count += 1
        
        return count
    
    def to_dict(self) -> Dict[str, Dict]:
        """Convert to dictionary format"""
        return {
            doc_key: asdict(version)
            for doc_key, version in self.versions.items()
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True)
    
    def to_simple_dict(self) -> Dict[str, str]:
        """Convert to simple doc_key -> semver mapping"""
        return {
            doc_key: version.semver
            for doc_key, version in self.versions.items()
        }
    
    def to_ledger_entry(self) -> Dict:
        """Format for ledger logging"""
        return {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'event': 'policy_snapshot',
            'documents': self.to_simple_dict(),
            'count': len(self.versions)
        }


def main():
    parser = argparse.ArgumentParser(
        description="Extract current versions of all versioned documents"
    )
    parser.add_argument(
        '--format',
        choices=['json', 'simple', 'ledger'],
        default='simple',
        help='Output format (default: simple)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        help='Output file (default: stdout)'
    )
    parser.add_argument(
        '--status',
        choices=['active', 'deprecated', 'frozen'],
        help='Filter by document status'
    )
    parser.add_argument(
        '--repo-root',
        type=Path,
        default=Path('.'),
        help='Repository root directory (default: current directory)'
    )
    
    args = parser.parse_args()
    
    # Extract document versions
    extractor = DocumentVersionExtractor(repo_root=args.repo_root)
    count = extractor.scan_documents(status_filter=args.status)
    
    # Format output
    if args.format == 'json':
        output = extractor.to_json()
    elif args.format == 'ledger':
        output = json.dumps(extractor.to_ledger_entry(), indent=2)
    else:  # simple
        output = json.dumps(extractor.to_simple_dict(), indent=2, sort_keys=True)
    
    # Write output
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output)
        print(f"✓ Wrote {count} document version(s) to {args.output}", file=sys.stderr)
    else:
        print(output)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
