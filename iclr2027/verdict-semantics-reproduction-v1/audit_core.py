"""Recompute the frozen comparison from recorded test-status maps, without tests."""
import argparse
import ast
import base64
from collections import Counter
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import re
from typing import Dict, List, Tuple


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def parse_status_maps(text):
    """Read only the exact map sections emitted by the frozen harness."""
    maps, declared, headers = {'before': {}, 'after': {}}, {}, Counter()
    stage, fallback = None, False
    for line in text.splitlines():
        if line == 'Tests BEFORE model patch':
            stage = 'before'
            headers[stage] += 1
        elif line == 'Tests AFTER model patch':
            stage = 'after'
            headers[stage] += 1
        elif line in ('Applying model patch', 'SUMMARY'):
            stage = None
        elif stage:
            count = re.fullmatch(r'Collected (\d+) test\(s\)', line)
            replacement = re.fullmatch(r'Fix-first fallback \(base image\): (\d+) result\(s\)', line)
            if replacement:
                if stage != 'before' or fallback:
                    raise ValueError('Unexpected fallback status section')
                maps[stage] = {}
                declared[stage] = int(replacement.group(1))
                fallback = True
            elif count:
                if stage in declared:
                    raise ValueError('Duplicate declared status-map count')
                declared[stage] = int(count.group(1))
            elif line.startswith('  ') and ': ' in line:
                test, status = line[2:].rsplit(': ', 1)
                if status not in ('PASSED', 'FAILED', 'ERROR', 'SKIPPED', 'TIMEOUT'):
                    raise ValueError('Unexpected recorded test status')
                if test in maps[stage]:
                    raise ValueError('Duplicate recorded test status')
                maps[stage][test] = status
    if headers != {'before': 1, 'after': 1} or set(declared) != {'before', 'after'}:
        raise ValueError('Missing or ambiguous before/after status map')
    if any(len(maps[k]) != declared[k] for k in maps):
        raise ValueError('Recorded status-map count mismatch')
    return maps, fallback


def original_functions(source):
    tree = ast.parse(source)
    compare = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'compare_results')
    evaluate = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'evaluate_instance')
    assignments = [n for n in ast.walk(evaluate) if isinstance(n, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == 'resolved' for t in n.targets)]
    if len(assignments) != 1:
        raise ValueError('Ambiguous frozen resolved assignment')
    namespace = {'Dict': Dict, 'List': List, 'Tuple': Tuple}
    # Only the source-bound pure comparison function and Boolean assignment run.
    # Container launch functions and received log content are never executed.
    exec(compile(ast.Module(body=[compare], type_ignores=[]), '<frozen-compare-results>', 'exec'), namespace)
    expression = compile(ast.Expression(assignments[0].value), '<frozen-resolved-rule>', 'eval')
    return namespace['compare_results'], expression, {
        'compare_results_source': ast.get_source_segment(source, compare),
        'resolved_assignment_source': ast.get_source_segment(source, assignments[0]),
        'resolved_assignment_line': assignments[0].lineno}


def audit(projection, verification, verdicts, source):
    compare, expression, code = original_functions(source)
    ids = verdicts['target_ids']
    if (len(ids) != 99 or len(set(ids)) != 99 or projection['target_ids'] != ids
            or projection['manifest_sha256'] != verdicts['manifest_sha256']
            or projection['harness_source_sha256'] != sha(source.encode())
            or set(projection['arms']) != set(verdicts['arms'])
            or set(projection['tasks']) != set(ids)):
        raise ValueError('Different frozen source or task population')
    blobs = {k: base64.b64decode(v, validate=True) for k, v in projection['blobs'].items()}
    if any(sha(v) != k for k, v in blobs.items()):
        raise ValueError('Changed original status artifact bytes')
    records, totals, exceptions, problems = {}, Counter(), [], []
    for arm, inputs in projection['arms'].items():
        if set(inputs) != set(ids):
            raise ValueError('Missing original condition record')
        rows = {}
        for iid in ids:
            original = verification['arms'][arm][iid]
            row = inputs[iid]
            if row['receipt_sha256'] != original['receipt_projection']['original_receipt_sha256']:
                raise ValueError('Different original receipt')
            expected = verdicts['arms'][arm]['records'][iid]
            result = {'official_resolved': expected['resolved'], 'errors': [], 'mode': row['mode']}
            totals['original_records'] += 1
            if row['mode'] == 'empty_submission_short_circuit':
                result['replay_scope'] = 'empty_submission_no_test_execution'
                totals['empty_predictions'] += 1
                rows[iid] = result
                continue
            totals['nonempty_official_reports'] += 1
            if row['files']['report.json'] != original['files']['report.json']:
                raise ValueError('Different original official report')
            report = json.loads(blobs[row['files']['report.json']])
            text = blobs[row['files']['test_output.txt']].decode()
            result.update(test_output_sha256=row['files']['test_output.txt'], report_sha256=row['files']['report.json'])
            if 'tests_status' not in report:
                if report['resolved'] is not False or report.get('failure_type') != 'verifier_setup_failed':
                    raise ValueError('Unrecognized original non-test report')
                result.update(replay_scope='original_setup_failure_no_complete_comparison', error=report['error'])
                totals['setup_failures'] += 1
                rows[iid] = result
                continue
            try:
                maps, fallback = parse_status_maps(text)
                task = projection['tasks'][iid]
                ftp, ptp = task['FAIL_TO_PASS'], task['PASS_TO_PASS']
                groups = compare(maps['before'], maps['after'], ftp, ptp)
                calculated = {'FAIL_TO_PASS': {'success': groups[0], 'failure': groups[1]},
                    'PASS_TO_PASS': {'success': groups[2], 'failure': groups[3]}}
                resolved = eval(expression, {}, {'f2p_success': groups[0], 'f2p_failure': groups[1], 'fail_to_pass_tests': ftp})
                if calculated != report['tests_status'] or resolved is not report['resolved'] or resolved is not expected['resolved']:
                    raise ValueError('Frozen test-map comparison differs from original report')
                nonpassing_success = []
                for test in groups[2]:
                    before, after = maps['before'].get(test, 'MISSING'), maps['after'].get(test, 'MISSING')
                    if after != 'PASSED':
                        nonpassing_success.append({'test': test, 'before': before, 'after': after})
                failures = [{'test': test, 'before': maps['before'].get(test, 'MISSING'),
                    'after': maps['after'].get(test, 'MISSING')} for test in groups[3]]
                result.update(replay_scope='complete_recorded_status_comparison',
                    parsed_counts={k: len(v) for k, v in maps.items()}, before_used_base_fallback=fallback,
                    fail_to_pass={'success': len(groups[0]), 'failure': len(groups[1])},
                    pass_to_pass={'success': len(groups[2]), 'failure': len(groups[3])},
                    pass_to_pass_failures=failures, pass_to_pass_success_without_after_passed=nonpassing_success)
                totals['exact_test_map_comparisons'] += 1
                totals['base_fallback_comparisons'] += int(fallback)
                totals['ptp_success_without_after_passed'] += len(nonpassing_success)
                if nonpassing_success:
                    totals['predictions_with_nonpassing_ptp_success'] += 1
                if resolved and failures:
                    exceptions.append({'arm': arm, 'instance_id': iid, 'official_resolved': True,
                        'pass_to_pass_failures': failures, 'report_sha256': result['report_sha256'],
                        'test_output_sha256': result['test_output_sha256']})
                if resolved and nonpassing_success:
                    totals['resolved_with_nonpassing_ptp_success'] += 1
            except (ValueError, KeyError, TypeError) as exc:
                result['errors'].append(str(exc))
                problems.append({'arm': arm, 'instance_id': iid, 'error': str(exc)})
            rows[iid] = result
        records[arm] = rows
    return {'benchmark': projection['benchmark'], 'manifest_sha256': projection['manifest_sha256'],
        'dataset_sha256': projection['dataset_sha256'], 'harness_source_sha256': projection['harness_source_sha256'],
        'target_ids': ids, 'totals': dict(totals), 'records': records,
        'official_resolved_with_ptp_failure': exceptions, 'comparison_errors': problems,
        'original_comparison_code': code,
        'limits': ['Replays recorded parsed test statuses, not complete raw runner stdout or test execution.',
            'Original empty predictions and setup failures remain in the fixed 594-record universe but have no complete status comparison.',
            'PASS_TO_PASS success in this frozen harness can include unchanged nonpassing statuses; resolved uses FAIL_TO_PASS only.',
            'No primary outcome replacement, rerun selection, benchmark pooling or causal memory inference.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise ValueError('Use a new audit output')
    plan = json.loads(args.plan.read_text())
    for name, expected in plan['files_sha256'].items():
        if sha(Path(name).read_bytes()) != expected:
            raise ValueError('Bound audit input changed: ' + name)
    projection = json.loads(gzip.decompress(Path(plan['projection']).read_bytes()))
    verification = json.loads(gzip.decompress(Path(plan['verification_projection']).read_bytes()))
    verdicts = json.loads(Path(plan['verdicts']).read_text())
    result = audit(projection, verification, verdicts, Path(plan['harness_source']).read_text())
    for name, expected in plan['files_sha256'].items():
        if sha(Path(name).read_bytes()) != expected:
            raise ValueError('Bound audit input changed during execution')
    result.update(at=datetime.now(timezone.utc).isoformat(), plan_sha256=sha(args.plan.read_bytes()))
    with args.out.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps({'totals': result['totals'], 'comparison_errors': result['comparison_errors'],
        'official_resolved_with_ptp_failure': result['official_resolved_with_ptp_failure']}))
    if result['comparison_errors']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
