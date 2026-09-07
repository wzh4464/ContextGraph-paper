"""Audit observed Related-Lite patch overlap over a fixed original-task universe.

This measures lexical overlap, not cheating, causal use, or source eligibility by
itself. Outcome values are not used. The replay needs only hashed edit features.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import re
import shlex
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
HUNK = re.compile(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@')
HEADER = re.compile(r'^\[GOLD PATCH src=([^\]\n]+)\][ \t]*$', re.M)
KINDS = ('prefix_added', 'added', 'signed', 'path_signed')
THRESHOLDS = (0.5, 0.7, 1.0)
ARMS = ('gfx-control', 'gfx-flat', 'gfx-skill', 'gfx-graph', 'gfx-rules', 'gfx-loc', 'gfx-skill2')


def encoded(obj):
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode()


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def sha(path):
    return digest(Path(path).read_bytes())


def save(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def edits(text):
    """Count only hunk-body edits; retain partial-hunk diagnostics explicitly."""
    values = {kind: set() for kind in KINDS}
    # Match the historical added-line text screen, independently of hunk syntax.
    values['prefix_added'] = {digest(line[1:].strip().encode()) for line in text.splitlines()
                              if line.startswith('+') and not line.startswith('+++') and line[1:].strip()}
    issues, files, pending, path, hunks = [], set(), None, None, 0
    for number, line in enumerate(text.splitlines(), 1):
        match = HUNK.match(line)
        if line.startswith('diff --git ') or match:
            if pending and any(pending):
                issues.append({'line': number, 'reason': 'interrupted_hunk', 'remaining': pending})
            pending = None
        if line.startswith('diff --git '):
            parts = shlex.split(line)
            path = parts[-1][2:] if len(parts) == 4 and parts[-1].startswith('b/') else None
        elif match:
            pending = [int(match.group(2) or 1), int(match.group(4) or 1)]
            hunks += 1
            if path is None:
                issues.append({'line': number, 'reason': 'hunk_without_path'})
        elif pending is not None and any(pending):
            if line.startswith('\\ No newline at end of file'):
                continue
            if not line or line[0] not in ' +-':
                issues.append({'line': number, 'reason': 'interrupted_hunk', 'remaining': pending})
                pending = None
                continue
            sign, body = line[0], line[1:]
            if sign in ' -':
                pending[0] -= 1
            if sign in ' +':
                pending[1] -= 1
            if min(pending) < 0:
                issues.append({'line': number, 'reason': 'hunk_count_underflow'})
                pending = None
                continue
            if sign in '+-' and body.strip():
                files.add(path)
                if sign == '+':
                    values['added'].add(digest(body.strip().encode()))
                values['signed'].add(digest((sign + body.strip()).encode()))
                # File/sign and exact nonblank body; indentation is retained here.
                values['path_signed'].add(digest(encoded([path, sign, body])))
    if pending and any(pending):
        issues.append({'reason': 'unfinished_hunk', 'remaining': pending})
    return {**{kind: sorted(value) for kind, value in values.items()},
            'issues': issues, 'hunks': hunks, 'changed_files': sorted(f for f in files if f is not None)}


def similarity(left, right):
    left, right = set(left), set(right)
    common, union = len(left & right), len(left | right)
    return {'intersection': common, 'union': union,
            'jaccard': common / union if left and right else 0.0}


def responses(history):
    queries, rows = set(), []
    for index, row in enumerate(history):
        if row.get('role') == 'assistant':
            for call in row.get('tool_calls') or []:
                if call.get('function', {}).get('name') == 'query_memory':
                    queries.add(call.get('id'))
        elif row.get('role') == 'tool':
            ids = row.get('tool_call_ids') or ([row['tool_call_id']] if row.get('tool_call_id') else [])
            matching = [key for key in ids if key in queries]
            if matching:
                text = row.get('content') or ''
                if not isinstance(text, str):
                    text = json.dumps(text)
                rows.append({'index': index, 'tool_call_ids': matching, 'text': text,
                             'sha256': digest(text.encode()),
                             'abstained': 'MEMORY_ABSTAINED' in text[:1000]})
    return rows


def blocks(text):
    matches = list(HEADER.finditer(text))
    return [(match.group(1).strip(), text[match.end():matches[index + 1].start()
              if index + 1 < len(matches) else len(text)].lstrip('\r\n'))
            for index, match in enumerate(matches)]


def pair_features(features, left, right, full_source=False):
    strict_valid = not features[left]['issues'] and (not full_source or not features[right]['issues'])
    return {kind: (similarity(features[left][kind], features[right][kind])
                   if kind == 'prefix_added' or strict_valid else
                   {'intersection': None, 'union': None, 'jaccard': None}) for kind in KINDS}


def replay(data):
    features, ids = data['features'], data['target_ids']
    if len(ids) != 99 or len(set(ids)) != 99 or set(data['records']) != set(ARMS):
        raise ValueError('Wrong fixed task universe')
    pool_rows, arm_rows, aggregate = {}, {}, {}
    for iid in ids:
        target = data['targets'][iid]
        pairs = []
        for sid, source in sorted(data['pool'].items()):
            pairs.append({'source_id': sid, 'same_repo': source['repo'] == target['repo'],
                          **pair_features(features, target['feature'], source['feature'], full_source=True)})
        pool_rows[iid] = {'maxima': maxima(pairs), 'pairs': pairs}
    for arm in ARMS:
        if set(data['records'][arm]) != set(ids):
            raise ValueError('Missing or extra original task')
        arm_rows[arm] = {}
        for iid in ids:
            target = data['targets'][iid]
            record = data['records'][arm][iid]
            pairs = [{**block, **pair_features(features, target['feature'], block['feature'])}
                     for block in record['blocks']]
            arm_rows[arm][iid] = {**record, 'blocks': pairs, 'maxima': maxima(pairs)}
        rows = list(arm_rows[arm].values())
        aggregate[arm] = {
            'targets': 99, 'targets_with_patch_blocks': sum(bool(r['blocks']) for r in rows),
            'responses': sum(r['responses'] for r in rows),
            'blocks': sum(len(r['blocks']) for r in rows),
            'blocks_with_parse_issues': sum(bool(features[b['feature']]['issues']) for r in rows for b in r['blocks']),
            'unknown_pool_sources': sorted({b['source_id'] for r in rows for b in r['blocks'] if b['source_id'] not in data['pool']}),
            'direct_target_source_ids': sorted({b['source_id'] for r in rows for b in r['blocks'] if b['source_id'] in ids}),
            'target_full_patch_literal_targets': [iid for iid in ids if any(b['target_full_patch_literal_present'] for b in arm_rows[arm][iid]['blocks'])],
            'observed_threshold_counts': threshold_counts(rows),
        }
    summary = {'benchmark': data['benchmark'], 'scope': data['scope'], 'arms': aggregate,
               'original_attempts': sum(r['targets'] for r in aggregate.values()),
               'pool_sources': len(data['pool']), 'pool_target_pairs': len(data['pool']) * len(ids),
               'pool_target_id_overlap': sorted(set(data['pool']) & set(ids)),
               'pool_threshold_counts': threshold_counts(list(pool_rows.values())),
               'historical_exclusion_ids': data['historical_exclusion_ids'],
               'targets_with_no_added_gold_lines': [iid for iid in ids if not features[data['targets'][iid]['feature']]['added']],
               'targets_with_incomplete_gold_hunks': [iid for iid in ids if features[data['targets'][iid]['feature']]['issues']],
               'pool_sources_with_incomplete_hunks': [sid for sid, row in data['pool'].items() if features[row['feature']]['issues']],
               'thresholds': list(THRESHOLDS), 'no_outcome_selection': True,
               'model_api_calls': 0, 'solver_or_verifier_runs': 0}
    return {'summary': summary, 'pool': pool_rows, 'arms': arm_rows}


def maxima(pairs):
    result = {}
    for scope in ('all_repos', 'same_repo'):
        selected = pairs if scope == 'all_repos' else [p for p in pairs if p['same_repo']]
        result[scope] = {}
        for kind in KINDS:
            maximum = max((p[kind]['jaccard'] for p in selected if p[kind]['jaccard'] is not None), default=None)
            result[scope][kind] = {'jaccard': maximum,
                'source_ids': sorted({p['source_id'] for p in selected if p[kind]['jaccard'] == maximum}) if maximum else []}
    return result


def threshold_counts(rows):
    return {scope: {kind: {str(t): sum(r['maxima'][scope][kind]['jaccard'] is not None
                and r['maxima'][scope][kind]['jaccard'] >= t for r in rows) for t in THRESHOLDS}
            for kind in KINDS} for scope in ('all_repos', 'same_repo')}


def collect(plan_path, output):
    import pandas as pd
    plan = json.loads(plan_path.read_bytes())
    for name, expected in plan['files_sha256'].items():
        if sha(ROOT / name) != expected:
            raise ValueError('Changed audit input/code: ' + name)
    inputs = ROOT / plan['inputs']
    table = pd.read_parquet(inputs / 'SWEContextBench_Related_Lite.parquet',
                           columns=['instance_id', 'repo', 'patch', 'base_commit'])
    target_rows = table.to_dict('records')
    manifest = json.loads((inputs / 'test99_patched.json').read_bytes())
    ids = sorted(r['instance_id'] for r in manifest)
    if len(ids) != 99 or sorted(r['instance_id'] for r in target_rows) != ids:
        raise ValueError('Pinned Related-Lite manifest/dataset mismatch')
    targets_raw = {r['instance_id']: r for r in target_rows}
    for row in manifest:
        if row['repo'] != targets_raw[row['instance_id']]['repo'] or row['base_commit'] != targets_raw[row['instance_id']]['base_commit']:
            raise ValueError('Target metadata mismatch')
    pool = json.loads((inputs / 'pool_gold_map.json').read_bytes())
    if len(pool) != 291 or sorted(pool) != sorted(json.loads((inputs / 'pool_ids_291.json').read_bytes())):
        raise ValueError('Wrong source snapshot')
    data = {'benchmark': 'SWEContextBench Related-Lite', 'scope': plan['scope'],
            'target_ids': ids, 'features': {}, 'targets': {}, 'pool': {}, 'records': {},
            'historical_exclusion_ids': plan['historical_exclusion_ids'], 'plan_sha256': sha(plan_path)}

    def feature(text, complete=False):
        obj = edits(text)
        if complete and not obj['hunks']:
            raise ValueError('Dataset patch has no recognizable hunk')
        key = digest(encoded(obj)); data['features'][key] = obj
        return key

    for iid, row in sorted(targets_raw.items()):
        data['targets'][iid] = {'repo': row['repo'], 'feature': feature(row['patch'], True),
                                'patch_sha256': digest(row['patch'].encode())}
    for sid, patch in sorted(pool.items()):
        data['pool'][sid] = {'repo': sid.rsplit('-', 1)[0].replace('__', '/'),
                            'feature': feature(patch, True), 'patch_sha256': digest(patch.encode())}
    bundle = ROOT / 'paper/iclr2027/delivery-reproduction-v1'
    compressed = (bundle / 'projection.json.gz').read_bytes()
    projection_raw = gzip.decompress(compressed)
    bindings = json.loads((bundle / 'source-bindings.json').read_bytes())
    if digest(projection_raw) != bindings['projection_sha256']:
        raise ValueError('Original projection binding differs')
    projection = json.loads(projection_raw)
    histories = projection['arms']
    expected = json.loads((bundle / 'expected-delivery.json').read_bytes())['arms']
    card2 = json.loads(gzip.decompress((inputs / 'card2-projection.json.gz').read_bytes()))
    card2_audit = json.loads((ROOT / 'docs/reports/gfx-skill2-completion-audit-20260906/completion-audit.json').read_bytes())
    if card2['target_ids'] != ids or projection['target_ids'] != ids:
        raise ValueError('Projection task universe differs')
    histories['gfx-skill2'] = card2['records']
    expected['gfx-skill2'] = card2_audit['delivery']['records']
    response_checks = 0
    for arm in ARMS:
        data['records'][arm] = {}
        for iid in ids:
            source, reference = histories[arm][iid], expected[arm][iid]
            if source['trajectory_sha256'] != reference['trajectory_sha256']:
                raise ValueError('Trajectory identity differs')
            actual = responses(source['history'])
            if [r['sha256'] for r in actual] != [r['response_sha256'] for r in reference.get('responses', [])]:
                raise ValueError('Response projection differs from original delivery census')
            response_checks += len(actual)
            record = {'trajectory_sha256': source['trajectory_sha256'], 'responses': len(actual),
                      'response_hashes': [r['sha256'] for r in actual], 'blocks': []}
            for response in actual:
                for index, (sid, body) in enumerate(blocks(response['text'])):
                    if response['abstained']:
                        raise ValueError('Abstention unexpectedly contains a source patch')
                    record['blocks'].append({'source_id': sid, 'same_repo': sid.rsplit('-', 1)[0].replace('__', '/') == targets_raw[iid]['repo'],
                        'response_sha256': response['sha256'], 'history_index': response['index'],
                        'block_index': index, 'body_sha256': digest(body.encode()), 'feature': feature(body),
                        'current_pool_full_patch_literal_present': bool(pool[sid].strip() in body) if sid in pool else None,
                        'target_full_patch_literal_present': targets_raw[iid]['patch'].strip() in body})
            data['records'][arm][iid] = record
        print(json.dumps({'projected_arm': arm, 'records': len(data['records'][arm])}), flush=True)
    output.mkdir(parents=True, exist_ok=False)
    raw = encoded(data)
    (output / 'audit-inputs.json.gz').write_bytes(gzip.compress(raw, mtime=0))
    result = replay(data)
    (output / 'results.json.gz').write_bytes(gzip.compress(encoded(result), mtime=0))
    save(output / 'summary.json', result['summary'])
    save(output / 'collection.json', {'at': datetime.now(timezone.utc).isoformat(),
        'plan_sha256': sha(plan_path), 'collector_sha256': sha(Path(__file__)),
        'original_trajectory_joins': 693, 'response_hash_joins': response_checks,
        'features': len(data['features']), 'audit_inputs_sha256': sha(output / 'audit-inputs.json.gz'),
        'results_sha256': sha(output / 'results.json.gz'), 'pandas_version': pd.__version__,
        'input_and_code_bindings_unchanged': all(sha(ROOT / name) == expected for name, expected in plan['files_sha256'].items())})
    print(json.dumps(result['summary']), flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    c = sub.add_parser('collect'); c.add_argument('--plan', type=Path, required=True); c.add_argument('--output', type=Path, required=True)
    r = sub.add_parser('reproduce'); r.add_argument('--directory', type=Path, required=True)
    a = p.parse_args()
    if a.command == 'collect':
        collect(a.plan, a.output)
    else:
        data = json.loads(gzip.decompress((a.directory / 'audit-inputs.json.gz').read_bytes()))
        expected = json.loads(gzip.decompress((a.directory / 'results.json.gz').read_bytes()))
        if replay(data) != expected:
            raise ValueError('Overlap replay differs')
        print(json.dumps({'replayed_original_attempts': 693, 'pool_target_pairs': 28809, 'all_results_match': True}))
