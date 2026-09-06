"""Recompute the supplied completed Related-Lite statistics without any service."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

sys.dont_write_bytecode = True
from paired_statistics import summarize


ARMS = ('gfx-control', 'gfx-flat', 'gfx-skill', 'gfx-graph', 'gfx-rules', 'gfx-loc')
FRAMES = ('primary99', 'historical_near_duplicate_sensitivity88')


def holm(rows, key):
    previous = 0.0
    for rank, row in enumerate(sorted(rows, key=lambda r: r['mcnemar_exact_two_sided_p'])):
        previous = max(previous, min(1.0, (len(rows) - rank) * row['mcnemar_exact_two_sided_p']))
        row[key] = previous


def recompute(data, expected):
    ids = data['target_ids']
    if len(ids) != 99 or len(set(ids)) != 99 or set(data['arms']) != set(ARMS):
        raise ValueError('Expected all six conditions and the full 99-task universe')
    if set(expected) != {'versus_flat', 'versus_control'}:
        raise ValueError('Expected both complete comparison families')
    if data['benchmark'] != 'SWEContextBench Related-Lite':
        raise ValueError('Different benchmark')
    for arm in data['arms'].values():
        rows = arm['records']
        if set(rows) != set(ids):
            raise ValueError('Missing or additional original attempt')
        if any(r.get('phase') != 'p1' or r.get('errors') or r.get('verification_valid') is not True
               or not isinstance(r.get('resolved'), bool) for r in rows.values()):
            raise ValueError('Invalid original first-prediction record')
    result = {}
    for family, source in expected.items():
        if set(source['frames']) != set(FRAMES):
            raise ValueError('Expected both fixed denominator frames')
        result[family] = {'benchmark': data['benchmark'], 'manifest_sha256': data['manifest_sha256'], 'frames': {}}
        for frame in FRAMES:
            excluded = source['frames'][frame]['excluded_ids']
            if (len(excluded) != (0 if frame == 'primary99' else 11)
                    or len(set(excluded)) != len(excluded) or not set(excluded) <= set(ids)
                    or excluded != expected['versus_control']['frames'][frame]['excluded_ids']):
                raise ValueError('Different or incomplete fixed sensitivity list')
            kept = [iid for iid in ids if iid not in excluded]
            selected = {**data, 'target_ids': kept,
                        'arms': {a: {'records': {iid: d['records'][iid] for iid in kept}}
                                 for a, d in data['arms'].items()}}
            left, rights = ('gfx-flat', ARMS[2:]) if family == 'versus_flat' else ('gfx-control', ARMS[1:])
            rows = [summarize(selected, left, right) for right in rights]
            holm(rows, 'holm_four_vs_flat_p' if family == 'versus_flat' else 'holm_five_vs_control_p')
            if family == 'versus_control':
                holm(rows[:2], 'holm_two_registered_vs_control_p')
            result[family]['frames'][frame] = {'excluded_ids': excluded, 'comparisons': rows}
    if result != expected:
        raise ValueError('Recomputed statistics differ from the source-bound published tables')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--out', type=Path, help='Optional new output file; existing files are never replaced')
    args = parser.parse_args()
    root = args.bundle.resolve()
    manifest = json.loads((root / 'manifest.json').read_text())
    if np.__version__ != manifest['numpy_version']:
        raise ValueError('Use the pinned NumPy version for exact bootstrap reproduction')
    for name, digest in manifest['files_sha256'].items():
        path = (root / name).resolve()
        if not path.is_relative_to(root) or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError('Bundle file hash mismatch: ' + name)
    data = json.loads((root / 'verdicts.json').read_text())
    expected = json.loads((root / 'expected-statistics.json').read_text())
    result = recompute(data, expected)
    if args.out:
        with args.out.open('x') as stream:
            json.dump(result, stream, indent=2)
            stream.write('\n')
    print(json.dumps({'records': sum(len(a['records']) for a in data['arms'].values()),
                      'comparisons_reproduced': 18, 'frames': [99, 88], 'all_statistics_match': True,
                      'scope': 'Statistical reproduction from supplied audited verdicts; raw verifier and memory audits are separate.'}))


if __name__ == '__main__':
    main()
