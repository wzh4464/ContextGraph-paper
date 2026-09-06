"""Verify supplied image manifest bytes without network, Docker or extraction."""
import argparse
import base64
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path

INDEX = {'application/vnd.oci.image.index.v1+json',
         'application/vnd.docker.distribution.manifest.list.v2+json'}
IMAGE = {'application/vnd.oci.image.manifest.v1+json',
         'application/vnd.docker.distribution.manifest.v2+json'}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def validate(images, observation, blobs):
    if len(images) != 100 or len({r['instance_id'] for r in images}) != 100:
        raise ValueError('Missing original base/task images')
    records = observation['records']
    if (observation['expected_images'] != 100 or len(records) != 100
            or len({r['instance_id'] for r in records}) != 100
            or {r['instance_id'] for r in records} != {r['instance_id'] for r in images}):
        raise ValueError('Different observation universe')
    source = {r['instance_id']: r for r in images}
    expected_blobs, objects, kinds, selected_children = set(), {}, Counter(), set()

    def document(digest, observed):
        key = digest.removeprefix('sha256:')
        expected_blobs.add(key)
        raw = blobs.get(key)
        if raw is None or sha(raw) != key:
            raise ValueError('Missing or changed raw manifest bytes')
        if (observed['http_status'] != 200 or observed['body_sha256'] != key
                or observed['body_bytes'] != len(raw)
                or observed['requested_digest_matches_bytes'] is not True):
            raise ValueError('Observation does not bind the raw manifest')
        if observed['header_digest_matches_request'] != (observed['docker_content_digest'] == digest):
            raise ValueError('Incorrect recorded header comparison')
        value = json.loads(raw)
        if value.get('schemaVersion') != 2:
            raise ValueError('Unexpected manifest schema')
        return value

    for row in records:
        original = source[row['instance_id']]
        for key in ('instance_id', 'reference', 'image_id', 'repo_digests', 'os', 'architecture'):
            if row[key] != original[key]:
                raise ValueError('Original image identity changed')
        if row['manifest_access_verified'] is not True:
            raise ValueError('Not all image manifests were verified')
        if 'jiayuanz3/swecontextbench@' + row['image_id'] not in row['repo_digests']:
            raise ValueError('Different frozen manifest identity')
        value = document(row['image_id'], row['root_manifest'])
        media = value.get('mediaType')
        if media in INDEX:
            kinds['platform_index'] += 1
            selected = [d for d in value.get('manifests', [])
                        if d.get('platform', {}).get('os') == row['os']
                        and d.get('platform', {}).get('architecture') == row['architecture']]
            if len(selected) != 1 or selected[0] != row['selected_platform_descriptor']:
                raise ValueError('Different or ambiguous selected platform')
            descriptor = selected[0]
            selected_children.add(descriptor['digest'])
            value = document(descriptor['digest'], row['platform_manifest'])
            if descriptor['size'] != row['platform_manifest']['body_bytes']:
                raise ValueError('Platform descriptor byte count mismatch')
            media = value.get('mediaType')
        else:
            kinds['single_image_manifest'] += 1
        if media not in IMAGE or not value.get('layers'):
            raise ValueError('Unsupported image manifest')
        if row['config_descriptor'] != value['config'] or row['layer_descriptors'] != value['layers']:
            raise ValueError('Recorded descriptors differ from downloaded bytes')
        descriptors = [value['config']] + value['layers']
        if row['config_and_compressed_layer_bytes'] != sum(d['size'] for d in descriptors):
            raise ValueError('Incorrect declared size')
        for descriptor in descriptors:
            digest, size = descriptor['digest'], descriptor['size']
            if (type(size) is not int or size < 0 or not digest.startswith('sha256:')
                    or len(digest) != 71 or any(c not in '0123456789abcdef' for c in digest[7:])):
                raise ValueError('Invalid descriptor')
            if digest in objects and objects[digest] != size:
                raise ValueError('Conflicting object lengths')
            objects[digest] = size
    if set(blobs) != expected_blobs:
        raise ValueError('Missing or additional manifest objects')
    return {'original_images': 100, 'raw_manifest_objects': len(blobs),
            'raw_manifest_bytes': sum(len(raw) for raw in blobs.values()),
            'root_manifest_kinds': dict(kinds), 'all_original_manifest_digests_match': True,
            'unique_selected_platform_manifests': len(selected_children),
            'unique_config_and_layer_descriptors': len(objects),
            'declared_compressed_object_bytes': sum(objects.values()),
            'scope': 'Original manifest bytes and descriptor inventory only. Config/layer payloads, single-manifest platform config, execution and availability after the recorded observation are not rechecked.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    root = args.bundle.resolve()
    manifest = json.loads((root / 'manifest.json').read_text())
    for name, digest in manifest['files_sha256'].items():
        path = (root / name).resolve()
        if not path.is_relative_to(root) or sha(path.read_bytes()) != digest:
            raise ValueError('Bundle file hash mismatch')
    projection = json.loads(gzip.decompress((root / 'raw-manifests.json.gz').read_bytes()))
    blobs = {digest: base64.b64decode(raw, validate=True) for digest, raw in projection['blobs_base64'].items()}
    result = validate(json.loads((root / 'images.json').read_text()),
                      json.loads((root / 'registry-observation.json').read_text()), blobs)
    print(json.dumps(result))


if __name__ == '__main__':
    main()
