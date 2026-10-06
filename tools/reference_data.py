"""Read core's published dataset artifacts without importing or running core.

Core owns acquisition, processing, selection and publication. Consumers reject
pending replacement and checksum mismatches, and work from immutable copies.
"""
import hashlib
import json
from pathlib import Path
import shutil

DATASETS = {'test_data': ('freemocap_test_data', 222), 'sample_data': ('freemocap_sample_data', 1108)}


def digest(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


def snapshot(prepared_root, dataset, output):
    name, expected_frames = DATASETS[dataset]
    root = Path(prepared_root) / name
    if (root / 'replacement.json').exists():
        raise ValueError('Pending dataset publication; use core datasets recover: ' + str(root))
    marker = root / 'ready.json'
    if not marker.is_file():
        raise FileNotFoundError('Prepare {} in core with poe process-{} first: {}'.format(dataset, dataset.replace('_', '-'), marker))
    marker_hash = digest(marker)
    ready = json.loads(marker.read_text(encoding='utf-8'))
    recording = Path(ready['recording']).resolve()
    recording.relative_to((root / 'current').resolve())
    if ready['identity']['source']['dataset'] != name:
        raise ValueError('Dataset identity does not match selected fixture')
    validation = ready['result']['validation']
    if validation['frames'] != expected_frames:
        raise ValueError('Prepared frame count does not match the reference dataset')
    source = recording / (name + '_data.parquet')
    before = digest(source)
    if before != validation['parquet_sha256']:
        raise ValueError('Parquet checksum differs from ready.json; revalidate in core: ' + str(source))
    calibration = recording / ready['result']['calibration_filename']
    calibration.resolve().relative_to(recording)
    calibration_hash = digest(calibration)
    if calibration_hash != ready['result']['calibration_sha256']:
        raise ValueError('Calibration checksum differs from ready.json')
    output = Path(output) / dataset
    output.mkdir(parents=True)
    destination = output / source.name
    shutil.copyfile(source, destination)
    if digest(destination) != before or digest(source) != before or digest(marker) != marker_hash or (root / 'replacement.json').exists():
        raise ValueError('Prepared recording changed while taking the test snapshot')
    (output / 'ready.json').write_text(json.dumps(ready, indent=2), encoding='utf-8')
    return dict(dataset=dataset, path=str(destination), source=str(source), sha256=before,
                marker=str(marker), marker_sha256=marker_hash, calibration=str(calibration),
                calibration_sha256=calibration_hash, frames=expected_frames,
                run_id=validation.get('run_id'), sensor_group=validation.get('sensor_group'),
                software=ready['identity'].get('software'), workflow=ready.get('workflow'))


def verify_unchanged(references):
    for reference in references:
        for path, expected in ((reference['source'], reference['sha256']),
                               (reference['path'], reference['sha256']),
                               (reference['marker'], reference['marker_sha256']),
                               (reference['calibration'], reference['calibration_sha256'])):
            if digest(path) != expected:
                raise ValueError('Reference changed during tests: ' + path)
        if (Path(reference['marker']).parent / 'replacement.json').exists():
            raise ValueError('Dataset replacement started during the test run')
