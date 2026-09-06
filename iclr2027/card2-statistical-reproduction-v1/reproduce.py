"""Recompute the separate adaptive Card-v2 comparisons from all original verdicts."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

sys.dont_write_bytecode = True
from paired_statistics import summarize

ARMS = ('gfx-flat', 'gfx-skill', 'gfx-skill2')
FRAMES = ('primary99', 'historical_near_duplicate_sensitivity88')
MANIFEST_SHA = '7bfa59a076575dd1d9a82f36b4875e8c7fef1a3d634f33e55311ceec99d51a87'


def recompute(data, expected):
    ids = data['target_ids']
    if (data['benchmark'] != 'SWEContextBench Related-Lite' or data['manifest_sha256'] != MANIFEST_SHA
            or len(ids) != 99 or len(set(ids)) != 99 or set(data['arms']) != set(ARMS)):
        raise ValueError('Expected the complete frozen three-condition universe')
    if set(expected['frames']) != set(FRAMES):
        raise ValueError('Expected both fixed frames')
    for arm in data['arms'].values():
        if set(arm['records']) != set(ids):
            raise ValueError('Missing or additional original attempt')
        for row in arm['records'].values():
            if (row.get('phase') != 'p1' or row.get('verification_valid') is not True
                    or row.get('errors') or not isinstance(row.get('resolved'), bool)):
                raise ValueError('Invalid original verdict')
    result = {k: data[k] for k in ('benchmark', 'manifest_sha256')}
    result['frames'] = {}
    for frame in FRAMES:
        excluded = expected['frames'][frame]['excluded_ids']
        if (len(excluded) != (0 if frame == 'primary99' else 11)
                or len(set(excluded)) != len(excluded) or not set(excluded) <= set(ids)):
            raise ValueError('Different fixed sensitivity list')
        kept = [iid for iid in ids if iid not in excluded]
        selected = {**data, 'target_ids': kept,
                    'arms': {a: {'records': {iid: rows['records'][iid] for iid in kept}}
                             for a, rows in data['arms'].items()}}
        rows = [summarize(selected, left, 'gfx-skill2') for left in ARMS[:2]]
        previous = 0.0
        for rank, row in enumerate(sorted(rows, key=lambda r: r['mcnemar_exact_two_sided_p'])):
            previous = max(previous, min(1.0, (2 - rank) * row['mcnemar_exact_two_sided_p']))
            row['holm_two_comparisons_p'] = previous
        result['frames'][frame] = {'excluded_ids': excluded, 'comparisons': rows}
    if result != expected:
        raise ValueError('Statistics differ from the original fixed analysis')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    root = args.bundle.resolve()
    manifest = json.loads((root / 'manifest.json').read_text())
    if np.__version__ != manifest['numpy_version']:
        raise ValueError('Use the pinned NumPy version for exact bootstrap reproduction')
    for name, expected in manifest['files_sha256'].items():
        path = (root / name).resolve()
        if not path.is_relative_to(root) or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Bundle input hash mismatch')
    result = recompute(json.loads((root / 'verdicts.json').read_text()),
                       json.loads((root / 'expected-statistics.json').read_text()))
    if args.out:
        with args.out.open('x') as stream:
            json.dump(result, stream, indent=2)
    print(json.dumps({'original_records': 297, 'comparisons_reproduced': 4,
                      'frames': [99, 88], 'all_statistics_match': True,
                      'scope': 'Separate adaptive Card-v2 statistics only; raw verification, delivery and source audits remain distinct.'}))


if __name__ == '__main__':
    main()
