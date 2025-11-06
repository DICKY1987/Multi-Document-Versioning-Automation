#!/usr/bin/env python3
"""
Example: Integrating Document Versioning with R_PIPELINE

This demonstrates how to capture active policy versions at the start
of every pipeline run for complete auditability.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from get_doc_versions import DocumentVersionExtractor


class PipelineRunManager:
    """Manages pipeline runs with policy version tracking"""
    
    def __init__(self, run_id: str, repo_root: Path = Path(".")):
        self.run_id = run_id
        self.repo_root = repo_root
        self.run_dir = repo_root / ".runs" / run_id
        self.run_dir.mkdir(parents=True, exist_ok=True)
    
    def capture_policy_snapshot(self) -> Dict:
        """
        Capture current versions of all active governance documents.
        
        This creates an immutable record of which policies/contracts
        were in force during this pipeline run.
        
        Returns:
            Dict containing policy snapshot
        """
        print(f"📋 Capturing policy snapshot for run {self.run_id}...")
        
        # Extract active document versions
        extractor = DocumentVersionExtractor(repo_root=self.repo_root)
        count = extractor.scan_documents(status_filter='active')
        
        # Create snapshot
        snapshot = {
            'run_id': self.run_id,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'event': 'policy_snapshot',
            'active_policies': extractor.to_simple_dict(),
            'policy_count': count,
            'full_details': extractor.to_dict()
        }
        
        # Save to run directory
        snapshot_path = self.run_dir / 'policy_snapshot.json'
        with open(snapshot_path, 'w') as f:
            json.dump(snapshot, f, indent=2, sort_keys=True)
        
        print(f"  ✓ Captured {count} active policies")
        print(f"  ✓ Saved to {snapshot_path}")
        
        return snapshot
    
    def append_to_ledger(self, event: Dict):
        """Append event to run ledger (append-only log)"""
        ledger_path = self.run_dir / 'ledger.jsonl'
        
        with open(ledger_path, 'a') as f:
            f.write(json.dumps(event) + '\n')
    
    def initialize_run(self):
        """Initialize pipeline run with policy tracking"""
        print(f"\n🚀 Initializing pipeline run: {self.run_id}")
        print(f"   Run directory: {self.run_dir}")
        
        # Capture policy snapshot
        snapshot = self.capture_policy_snapshot()
        
        # Log to ledger
        self.append_to_ledger(snapshot)
        
        # Create run metadata
        metadata = {
            'run_id': self.run_id,
            'start_time': datetime.utcnow().isoformat() + 'Z',
            'policies_in_force': snapshot['active_policies'],
            'policy_count': snapshot['policy_count']
        }
        
        metadata_path = self.run_dir / 'metadata.json'
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\n✅ Run initialized with policy tracking")
        print(f"   Policies in force:")
        for doc_key, version in snapshot['active_policies'].items():
            print(f"     • {doc_key}: v{version}")
        
        return metadata
    
    def finalize_run(self, success: bool):
        """Finalize pipeline run"""
        metadata_path = self.run_dir / 'metadata.json'
        with open(metadata_path) as f:
            metadata = json.load(f)
        
        metadata['end_time'] = datetime.utcnow().isoformat() + 'Z'
        metadata['success'] = success
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Log completion to ledger
        self.append_to_ledger({
            'run_id': self.run_id,
            'timestamp': metadata['end_time'],
            'event': 'run_complete',
            'success': success
        })
        
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"\n{status}: Run {self.run_id} complete")


def example_run():
    """Example pipeline run with policy tracking"""
    
    # Generate run ID (using simple timestamp for example)
    run_id = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    
    # Create run manager
    manager = PipelineRunManager(run_id)
    
    try:
        # Initialize run (captures policy snapshot)
        metadata = manager.initialize_run()
        
        # Your pipeline logic here
        print("\n⚙️  Executing pipeline tasks...")
        print("   • Task 1: File classification")
        print("   • Task 2: Validation")
        print("   • Task 3: Auto-fix")
        print("   ✓ All tasks complete")
        
        # Finalize run
        manager.finalize_run(success=True)
        
    except Exception as e:
        print(f"\n❌ Error during run: {e}")
        manager.finalize_run(success=False)
        raise


def query_historical_policies(run_id: str):
    """
    Query which policies were in force during a specific run.
    
    This is how you answer: "What rules were active when run X executed?"
    """
    print(f"\n🔍 Querying policies for run: {run_id}")
    
    run_dir = Path('.runs') / run_id
    snapshot_path = run_dir / 'policy_snapshot.json'
    
    if not snapshot_path.exists():
        print(f"❌ No snapshot found for run {run_id}")
        return
    
    with open(snapshot_path) as f:
        snapshot = json.load(f)
    
    print(f"\n📋 Policies in force during run {run_id}:")
    print(f"   Timestamp: {snapshot['timestamp']}")
    print(f"   Policy count: {snapshot['policy_count']}")
    print(f"\n   Active policies:")
    
    for doc_key, version in sorted(snapshot['active_policies'].items()):
        print(f"     • {doc_key}: v{version}")
        
        # Show how to checkout that exact version
        tag = f"docs-{doc_key}-{version}"
        print(f"       → git checkout {tag}")
    
    return snapshot


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'query':
        # Query mode: python example_integration.py query <run_id>
        if len(sys.argv) < 3:
            print("Usage: python example_integration.py query <run_id>")
            sys.exit(1)
        query_historical_policies(sys.argv[2])
    else:
        # Run mode: python example_integration.py
        example_run()
