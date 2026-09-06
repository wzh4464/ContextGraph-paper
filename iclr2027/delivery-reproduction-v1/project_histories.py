"""Read completed trajectories into a private, source-bound delivery projection."""
import argparse
import hashlib
import json
from pathlib import Path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def project(history, control):
    result, queries, first_user = [], set(), False
    for original in history:
        role = original.get('role')
        row = {'role': role}
        if control and (role == 'system' or (role == 'user' and not first_user)):
            row['content'] = original.get('content')
            if role == 'user':
                first_user = True
        if role == 'assistant':
            if control:
                row['action'] = original.get('action')
            calls = []
            for call in original.get('tool_calls') or []:
                function = call.get('function') or {}
                value = {'id': call.get('id'), 'function': {'name': function.get('name')}}
                if function.get('name') == 'query_memory':
                    queries.add(call.get('id'))
                    value['function']['arguments'] = function.get('arguments', {})
                calls.append(value)
            row['tool_calls'] = calls
        elif role == 'tool' and not control:
            ids = original.get('tool_call_ids') or ([original['tool_call_id']] if original.get('tool_call_id') else [])
            row['tool_call_ids'] = ids
            if any(i in queries for i in ids):
                row['content'] = original.get('content')
        result.append(row)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text())
    cards_path = Path(plan['cards_path'])
    if sha(cards_path) != plan['cards_sha256']:
        raise ValueError('Original card file changed')
    cards = json.loads(cards_path.read_text())
    if len(plan['target_ids']) != 99 or len(set(plan['target_ids'])) != 99 or len(plan['arms']) != 6:
        raise ValueError('Require all 594 completed original attempts')
    result = {'benchmark': plan['benchmark'], 'manifest_sha256': plan['manifest_sha256'],
              'target_ids': plan['target_ids'], 'cards_sha256': plan['cards_sha256'],
              'export_source_sha256': sha(Path(__file__)), 'arms': {}}
    for arm, rows in plan['arms'].items():
        if set(rows) != set(plan['target_ids']):
            raise ValueError('Different source task universe')
        result['arms'][arm] = {}
        for index, iid in enumerate(plan['target_ids'], 1):
            source = rows[iid]
            path = Path(source['trajectory_path'])
            raw = path.read_bytes()
            if hashlib.sha256(raw).hexdigest() != source['trajectory_sha256']:
                raise ValueError('Original trajectory changed: ' + arm + ':' + iid)
            data = json.loads(raw)
            history = data.get('history') or []
            if not history:
                raise ValueError('Missing original history')
            repo = iid.rsplit('-', 1)[0].replace('__', '/')
            expected_card = None
            if arm == 'gfx-skill':
                matches = [c['card'] for c in cards['cards'].values()
                           if c['card'].startswith('[REPO PLAYBOOK — ' + repo + ' ·')]
                if len(matches) != 1:
                    raise ValueError('Missing or ambiguous frozen card')
                expected_card = matches[0]
            result['arms'][arm][iid] = {'trajectory_sha256': source['trajectory_sha256'],
                'original_history_length': len(history), 'repo': repo,
                'expected_card': expected_card, 'history': project(history, arm == 'gfx-control')}
            if sha(path) != source['trajectory_sha256']:
                raise ValueError('Original trajectory changed during projection')
            if index % 25 == 0:
                print(arm + ': ' + str(index) + ' original histories projected', flush=True)
        print(arm + ': complete', flush=True)
    if sha(cards_path) != plan['cards_sha256']:
        raise ValueError('Frozen cards changed during projection')
    with args.out.open('x') as stream:
        json.dump(result, stream, ensure_ascii=False)
    args.out.chmod(0o600)
    print('projection complete; sha256=' + sha(args.out), flush=True)


if __name__ == '__main__':
    main()
