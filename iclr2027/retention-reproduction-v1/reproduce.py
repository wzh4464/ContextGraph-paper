"""Reproduce original response retention from source-bound structural histories."""
import argparse
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True


def load_processor(root):
    spec = importlib.util.spec_from_file_location('retention_core', root / 'retention_core.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.ReplayProcessor


def reconstruct(row, processor_type):
    processor = processor_type(row['recorded_processor'])
    history, responses = [], []
    for index, entry in enumerate(row['history']):
        h = {k: entry[k] for k in ('role', 'agent', 'message_type', 'is_demo', 'tags') if k in entry}
        if h.get('agent') != 'main':
            raise ValueError('Unsupported agent filtering')
        response = entry.get('served_response')
        h['content'] = ''
        if response:
            if response['lines'] <= 0 or response['chars'] <= 0:
                raise ValueError('Empty served response')
            # Shape placeholder, not generated agent text. Only retention identity
            # and the original response's omitted-line count are reconstructed.
            h['content'] = 'response-sha256:' + response['sha256'] + '\n' * response['lines']
            assert len(h['content'].splitlines()) == response['lines']
            responses.append({'history_index': index, 'response_sha256': response['sha256'],
                              'original_chars': response['chars'], 'tags': h.get('tags', []),
                              'message_type': h.get('message_type')})
        history.append(h)
    positions = [r['history_index'] for r in responses]
    actions = [i for i, h in enumerate(history) if h.get('role') == 'assistant' and h.get('message_type') == 'action']
    states = []
    for end in actions:
        omitted = set(processor._get_omit_indices(history[:end]))
        states.append([i for i in positions if i < end
                       and not set(history[i].get('tags', [])) & processor.always_remove_output_for_tags
                       and (i not in omitted or set(history[i].get('tags', [])) & processor.always_keep_output_for_tags)])
    intervals = []
    for ordinal, state in enumerate(states, 1):
        if intervals and intervals[-1]['retained_response_indices'] == state:
            intervals[-1]['last_recorded_action_number'] = ordinal
        else:
            intervals.append({'first_recorded_action_number': ordinal,
                              'last_recorded_action_number': ordinal, 'retained_response_indices': state})
    boundaries = {0, len(actions) - 1} if actions else set()
    boundaries.update(i for i in range(1, len(states)) if states[i] != states[i - 1])
    boundaries.update(i - 1 for i in list(boundaries) if i > 0)
    checks = []
    for ordinal in sorted(boundaries):
        end = actions[ordinal]
        rendered = processor(history[:end])
        retained = [i for i in positions if i < end and rendered[i]['content'] == history[i]['content']]
        if retained != states[ordinal]:
            raise ValueError('Reconstruction disagrees with original processor methods')
        checks.append({'recorded_action_number': ordinal + 1, 'history_prefix_end': end,
                       'retained_response_indices': retained,
                       'omitted_responses': [{'history_index': i, 'processed_content': rendered[i]['content']}
                                            for i in positions if i < end and i not in retained]})
    visible = [i + 1 for i, state in enumerate(states) if state]
    return {'trajectory_sha256': row['trajectory_sha256'], 'recorded_processor': row['recorded_processor'],
            'recorded_action_prefixes': len(actions), 'served_memory_response_count': len(positions),
            'responses': responses,
            'prefixes_after_first_memory_response': sum(bool(positions) and end > positions[0] for end in actions),
            'prefixes_retaining_any_original_memory_response': len(visible),
            'first_visible_recorded_action_number': visible[0] if visible else None,
            'last_visible_recorded_action_number': visible[-1] if visible else None,
            'last_action_retains_original_memory_response': bool(states[-1]) if states else None,
            'retention_intervals': intervals, 'original_processor_boundary_checks': checks}


def reproduce(projection, expected, attempts, processor_type):
    ids = projection['target_ids']
    if len(ids) != 99 or len(set(ids)) != 99:
        raise ValueError('Require all 99 fixed targets')
    for source in (projection, expected, attempts):
        if (source['target_ids'] != ids or source['benchmark'] != 'SWEContextBench Related-Lite'
                or source['manifest_sha256'] != projection['manifest_sha256']
                or set(source['arms']) != {'gfx-flat', 'gfx-skill'}):
            raise ValueError('Different fixed benchmark/arm universe')
        for rows in source['arms'].values():
            if set(rows) != set(ids):
                raise ValueError('Missing original trajectory record')
    summary = {}
    for arm in projection['arms']:
        records = []
        for iid, row in projection['arms'][arm].items():
            attempt = attempts['arms'][arm][iid]
            if (attempt['phase'] != 'p1' or attempt['verification_valid'] is not True
                    or attempt['errors'] or attempt['trajectory_sha256'] != row['trajectory_sha256']):
                raise ValueError('Different original prediction evidence')
            record = reconstruct(row, processor_type)
            if record != expected['arms'][arm][iid]:
                raise ValueError('Retention record differs: ' + arm + ':' + iid)
            records.append(record)
        summary[arm] = {'records': len(records),
                        'ever_served_memory': sum(bool(r['served_memory_response_count']) for r in records),
                        'retained_at_last_action': sum(r['last_action_retains_original_memory_response'] for r in records),
                        'original_processor_boundary_checks': sum(len(r['original_processor_boundary_checks']) for r in records)}
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
    raw = gzip.decompress((root / 'projection.json.gz').read_bytes())
    sources = json.loads((root / 'source-bindings.json').read_text())
    if hashlib.sha256(raw).hexdigest() != sources['projection_sha256']:
        raise ValueError('Changed structural projection')
    summary = reproduce(json.loads(raw), json.loads((root / 'expected-retention.json').read_text()),
                        json.loads((root / 'original-attempts.json').read_text()), load_processor(root))
    print(json.dumps({'records_reproduced': 198, 'summary': summary,
                      'scope': 'Original processor methods on source-bound structural histories. No original free text or every-wire-request reconstruction; delivery content and official verifier execution are separate evidence.'}))


if __name__ == '__main__':
    main()
