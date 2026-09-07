"""Reproduce the fixed all-task patch-overlap audit from hashed edit features."""
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / 'manifest.json').read_bytes())
    expected_files = {'README.md', 'reproduce.py', 'overlap_core.py', 'audit-inputs.json.gz',
                      'expected-results.json.gz', 'source-bindings.json'}
    if set(manifest['files_sha256']) != expected_files:
        raise ValueError('Missing or extra package binding')
    for name, expected in manifest['files_sha256'].items():
        if hashlib.sha256((root / name).read_bytes()).hexdigest() != expected:
            raise ValueError('Changed package file: ' + name)
    spec = importlib.util.spec_from_file_location('overlap_core', root / 'overlap_core.py')
    core = importlib.util.module_from_spec(spec); spec.loader.exec_module(core)
    data = json.loads(gzip.decompress((root / 'audit-inputs.json.gz').read_bytes()))
    expected = json.loads(gzip.decompress((root / 'expected-results.json.gz').read_bytes()))
    if core.replay(data) != expected:
        raise ValueError('Computed overlaps differ from the complete recorded result')
    print(json.dumps({'original_attempts': 693, 'conditions': 7, 'tasks_per_condition': 99,
                      'pool_sources': 291, 'pool_target_pairs': 28809,
                      'all_results_match': True, 'model_api_calls': 0,
                      'solver_or_verifier_runs': 0}))


if __name__ == '__main__':
    main()
