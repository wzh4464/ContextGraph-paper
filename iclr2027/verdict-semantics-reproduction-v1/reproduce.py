"""Offline reproduction of frozen verdict semantics over original recorded statuses."""
import argparse
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    if args.out and args.out.exists():
        raise ValueError('Use a new output path')
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / 'manifest.json').read_text())
    for name, expected in manifest['files_sha256'].items():
        if Path(name).name != name or hashlib.sha256((root / name).read_bytes()).hexdigest() != expected:
            raise ValueError('Bundle file integrity mismatch: ' + name)
    spec = importlib.util.spec_from_file_location('frozen_status_audit_core', root / 'audit_core.py')
    core = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(core)
    projection = json.loads(gzip.decompress((root / 'projection.json.gz').read_bytes()))
    identities = json.loads((root / 'verification-identities.json').read_text())
    verdicts = json.loads((root / 'verdicts.json').read_text())
    result = core.audit(projection, identities, verdicts, (root / 'original_run_evaluation.py').read_text())
    if result['comparison_errors']:
        raise ValueError('Frozen comparison disagrees with original reports')
    if result != json.loads((root / 'expected-audit.json').read_text()):
        raise ValueError('Reproduced status audit differs from original audit')
    if args.out:
        with args.out.open('x') as stream:
            json.dump(result, stream, indent=2)
            stream.write('\n')
    print(json.dumps({'totals': result['totals'], 'comparison_errors': result['comparison_errors'],
        'official_resolved_with_ptp_failure': result['official_resolved_with_ptp_failure']}, indent=2))


if __name__ == '__main__':
    main()
