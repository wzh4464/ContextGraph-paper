"""Recheck delivered memory content and direct Control exposure from supplied fields."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
from delivery_core import inspect, inspect_history

ARMS = {'gfx-control', 'gfx-flat', 'gfx-skill', 'gfx-graph', 'gfx-rules', 'gfx-loc'}


def reproduce(projection, expected, verdicts):
    ids = projection['target_ids']
    if (len(ids) != 99 or len(set(ids)) != 99 or set(projection['arms']) != ARMS
            or set(expected['arms']) != ARMS or set(verdicts['arms']) != ARMS
            or projection['benchmark'] != 'SWEContextBench Related-Lite'
            or projection['manifest_sha256'] != verdicts['manifest_sha256']
            or set(ids) != set(verdicts['target_ids'])):
        raise ValueError('Different benchmark or missing original task/arm universe')
    observed = {}
    summary = {}
    for arm, records in projection['arms'].items():
        if (set(records) != set(ids) or set(expected['arms'][arm]) != set(ids)
                or set(verdicts['arms'][arm]['records']) != set(ids)):
            raise ValueError('Incomplete task/arm records')
        observed[arm] = {}
        for iid, row in records.items():
            history = row['history']
            if not history or len(history) != row['original_history_length']:
                raise ValueError('Missing projected history entries')
            verdict = verdicts['arms'][arm]['records'][iid]
            if (row['trajectory_sha256'] != verdict['trajectory_sha256']
                    or verdict.get('verification_valid') is not True or verdict.get('errors')
                    or verdict.get('phase') != 'p1'):
                raise ValueError('Delivery and verdict belong to different original evidence')
            if arm == 'gfx-control':
                audit = inspect(history)
                audit.update(trajectory_sha256=row['trajectory_sha256'],
                             errors=[] if audit['no_direct_memory_observed'] else ['direct_memory_exposure_or_missing_prompt'])
            else:
                audit = inspect_history(history, row['expected_card'])
                audit['trajectory_sha256'] = row['trajectory_sha256']
                if arm in ('gfx-flat', 'gfx-skill'):
                    audit['repo'] = row['repo']
                    audit['wrong_repo_card_headers'] = [h for r in audit['responses'] for h in r['card_headers'] if h != row['repo']]
                else:
                    texts = {hashlib.sha256(h['content'].encode()).hexdigest(): h['content'] for h in history
                             if h.get('role') == 'tool' and isinstance(h.get('content'), str)}
                    for response in audit['responses']:
                        text = texts[response['response_sha256']]
                        response['rule_ids'] = re.findall(r'^\[(rule_[0-9a-f]+)\]\s+\S', text, re.M)
                        marker = re.search(r'^\[LIKELY FILES[^\n]*\]\n', text, re.M)
                        response['likely_file_paths'] = re.findall(r'^\s*\d+\. ([^\n]+?) \(\d+\)\s*$', text[marker.end():], re.M) if marker else []
                        response['likely_files_nonempty'] = bool(response['likely_file_paths'])
                        response['target_id_patch_sources'] = sorted(set(response['source_ids']) & set(ids))
                    audit['errors'] = []
            if audit != expected['arms'][arm][iid]:
                raise ValueError('Recomputed delivery record differs: ' + arm + ':' + iid)
            observed[arm][iid] = audit
        if arm == 'gfx-control':
            summary[arm] = {'n': 99, 'no_direct_memory_targets': sum(r['no_direct_memory_observed'] for r in observed[arm].values())}
        else:
            summary[arm] = {'n': 99, 'served_targets': sum(r['served'] for r in observed[arm].values()),
                'served_pre_plan_targets': sum(r['served_pre_plan'] for r in observed[arm].values()),
                'phase_refusals': sum(r['phase_refusals'] for r in observed[arm].values())}
            if arm == 'gfx-skill':
                summary[arm]['exact_repo_card_targets'] = sum(r['exact_card_served'] for r in observed[arm].values())
    if summary != expected['summary']:
        raise ValueError('Recomputed delivery counts differ')
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    root = args.bundle.resolve()
    manifest = json.loads((root / 'manifest.json').read_text())
    for name, digest in manifest['files_sha256'].items():
        path = (root / name).resolve()
        if not path.is_relative_to(root) or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError('Bundle hash mismatch: ' + name)
    raw_projection = gzip.decompress((root / 'projection.json.gz').read_bytes())
    sources = json.loads((root / 'source-bindings.json').read_text())
    if hashlib.sha256(raw_projection).hexdigest() != sources['projection_sha256']:
        raise ValueError('Decompressed projection differs from the original transfer')
    projection = json.loads(raw_projection)
    expected, verdicts = [json.loads((root / name).read_text()) for name in
                          ('expected-delivery.json', 'verdicts.json')]
    print(json.dumps({'records_reproduced': 594, 'summary': reproduce(projection, expected, verdicts),
                      'scope': 'Original classifier checks over source-bound projected fields. Raw verifier, debug-log rate limits and unrecorded memory channels are not re-audited.'}))


if __name__ == '__main__':
    main()
