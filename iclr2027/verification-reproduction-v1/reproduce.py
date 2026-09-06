"""Offline original-prediction/report replay; no benchmark execution or model calls."""
import argparse
import base64
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def reproduce(root):
    manifest = json.loads((root / 'manifest.json').read_text())
    for name, digest in manifest['files_sha256'].items():
        if Path(name).name != name or sha((root / name).read_bytes()) != digest:
            raise ValueError('Bundle file identity mismatch: ' + name)
    spec = importlib.util.spec_from_file_location('bound_verification_core', root / 'verification_core.py')
    core = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(core)
    projection = json.loads(gzip.decompress((root / 'projection.json.gz').read_bytes()))
    verdicts = json.loads((root / 'verdicts.json').read_text())
    sources = json.loads((root / 'source-bindings.json').read_text())
    ids = verdicts['target_ids']
    if (len(ids) != 99 or len(set(ids)) != 99 or projection['target_ids'] != ids
            or projection['manifest_sha256'] != verdicts['manifest_sha256']
            or projection['benchmark'] != verdicts['benchmark']):
        raise ValueError('Different or incomplete frozen task universe')
    arms = {'gfx-control', 'gfx-flat', 'gfx-skill', 'gfx-graph', 'gfx-rules', 'gfx-loc'}
    if set(projection['arms']) != arms or set(verdicts['arms']) != arms:
        raise ValueError('Missing or unexpected experimental condition')
    blobs = {key: base64.b64decode(value, validate=True) for key, value in projection['blobs'].items()}
    if any(sha(raw) != key for key, raw in blobs.items()):
        raise ValueError('Original artifact byte hash mismatch')
    used, output, predictions, exceptions = set(), {}, {}, []
    for arm in sorted(arms):
        rows = projection['arms'][arm]
        if set(rows) != set(ids) or set(verdicts['arms'][arm]['records']) != set(ids):
            raise ValueError('Missing original prediction record')
        counts = {'records': 0, 'resolved': 0, 'nonempty_official_reports': 0, 'empty_predictions': 0}
        predictions[arm] = []
        for iid in ids:
            row = rows[iid]
            receipt, files = row['receipt_projection'], row['files']
            audited = verdicts['arms'][arm]['records'][iid]
            if (receipt['iid'] != iid or receipt['pass_tag'] != 'p1'
                    or receipt['verification_valid'] is not True
                    or type(receipt['resolved']) is not bool
                    or receipt['original_receipt_sha256'] != sources['original_receipts_sha256'][arm][iid]):
                raise ValueError('Original receipt identity mismatch')
            for name in ('resolved', 'trajectory_sha256', 'prediction_sha256', 'submission_sha256', 'exit_status', 'harness_commit'):
                if receipt[name] != audited[name]:
                    raise ValueError('Export differs from bound first-prediction audit: ' + name)
            if receipt['verification_mode'] != audited['mode']:
                raise ValueError('Original verification mode mismatch')
            used.update(files.values())
            raw_prediction = blobs[files['prediction.json']]
            if sha(raw_prediction) != audited['prediction_sha256']:
                raise ValueError('Not the original prediction bytes')
            prediction = json.loads(raw_prediction)
            patch = prediction.get('model_patch') or ''
            if prediction['instance_id'] != iid or sha(patch.encode()) != audited['submission_sha256']:
                raise ValueError('Prediction task or patch mismatch')
            if patch.strip():
                if (set(files) != {'prediction.json', 'report.json', 'result.json', 'patch.diff'}
                        or receipt['verification_mode'] != 'official_harness'
                        or receipt['submission_nonempty'] is not True
                        or blobs[files['patch.diff']] != patch.encode()):
                    raise ValueError('Verified patch identity or mode mismatch')
                projected = receipt['harness_evidence_projection']['files']
                if len(projected) != 3 or {r['name'] for r in projected} != {'report.json', 'result.json', 'patch.diff'}:
                    raise ValueError('Incomplete official evidence projection')
                for entry in projected:
                    raw = blobs[files[entry['name']]]
                    if sha(raw) != entry['sha256'] or len(raw) != entry['bytes']:
                        raise ValueError('Original official artifact identity mismatch')
                report = json.loads(blobs[files['report.json']])
                result = json.loads(blobs[files['result.json']])
                if (not core.report_matches(report, iid, audited['resolved'])
                        or not core.report_matches(result.get(iid, {}), iid, audited['resolved'])
                        or result[iid] != report):
                    raise ValueError('Original official report disagrees with audited verdict')
                counts['nonempty_official_reports'] += 1
            else:
                if (set(files) != {'prediction.json'} or receipt['resolved'] is not False
                        or receipt['submission_nonempty'] is not False
                        or receipt['verification_mode'] != 'empty_submission_short_circuit'):
                    raise ValueError('Empty-prediction mode or outcome mismatch')
                expected = {'kind': 'v14_official_offline_docker_attestation_v1', 'passed': True,
                    'zero_docker_exemption': True, 'reason': 'empty_submission_short_circuit',
                    'audit_record_count': 0, 'container_inspect_record_count': 0}
                actual = receipt['empty_exemption_projection']
                if any(type(actual.get(k)) is not type(v) or actual.get(k) != v for k, v in expected.items()):
                    raise ValueError('Original empty-prediction exemption mismatch')
                counts['empty_predictions'] += 1
            if audited.get('historical_audit_errors'):
                exceptions.append({'arm': arm, 'instance_id': iid,
                    'historical_audit_errors': audited['historical_audit_errors'],
                    'verification_evidence_origin': audited.get('verification_evidence_origin'),
                    'recheck_receipt_sha256': audited.get('recheck_receipt_sha256')})
            counts['records'] += 1
            counts['resolved'] += int(audited['resolved'])
            predictions[arm].append(prediction)
        output[arm] = counts
    if used != set(blobs):
        raise ValueError('Unreferenced or missing raw artifact blob')
    summary = {'records': sum(v['records'] for v in output.values()),
        'nonempty_official_reports': sum(v['nonempty_official_reports'] for v in output.values()),
        'empty_predictions': sum(v['empty_predictions'] for v in output.values()),
        'original_artifact_blobs': len(blobs), 'arms': output, 'historical_exceptions': exceptions}
    if summary != json.loads((root / 'expected-verification.json').read_text()):
        raise ValueError('Recomputed report/patch coverage differs from frozen expected results')
    return summary, predictions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--predictions-dir', type=Path)
    args = parser.parse_args()
    if (args.out and args.out.exists()) or (args.predictions_dir and args.predictions_dir.exists()):
        raise ValueError('Use new output paths')
    summary, predictions = reproduce(Path(__file__).resolve().parent)
    if args.predictions_dir:
        args.predictions_dir.mkdir(parents=True, exist_ok=False)
        for arm, rows in predictions.items():
            with (args.predictions_dir / (arm + '.jsonl')).open('x') as stream:
                for row in rows:
                    stream.write(json.dumps(row, ensure_ascii=False) + '\n')
    if args.out:
        with args.out.open('x') as stream:
            json.dump(summary, stream, indent=2)
            stream.write('\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
