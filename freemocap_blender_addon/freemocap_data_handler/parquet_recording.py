"""Read the self-contained recording contract, without producer-package imports.

Coordinates cross the Blender boundary here: mm -> m, world wxyz unchanged.
Mapped keypoints are observations; landmarks are rigidified model trajectories.
"""
import json
from pathlib import Path

import numpy as np

from ..utilities.dependencies import parquet_module


def recording_file(path):
    path = Path(path)
    if path.is_file() and path.suffix.lower() == '.parquet':
        return path
    files = sorted(path.glob('*_data.parquet')) if path.is_dir() else []
    if len(files) != 1:
        raise ValueError('Select one recording Parquet file, or a folder containing exactly one *_data.parquet')
    return files[0]


def read_recording(path, *, trajectory_channel='LANDMARKS_3D', segments=True,
                   run_id=None, sensor_group=None):
    if trajectory_channel not in ('LANDMARKS_3D', 'MAPPED_KEYPOINTS_3D'):
        raise ValueError('Expected landmarks or mapped keypoints')
    parquet = parquet_module()
    path = recording_file(path)
    metadata = parquet.read_schema(path).metadata or {}
    if b'freemocap.recording' not in metadata:
        raise ValueError('Missing freemocap.recording metadata')
    descriptor = json.loads(metadata[b'freemocap.recording'])
    if descriptor['schema_version'] != 1:
        raise ValueError('Unsupported recording schema version')
    run_id = descriptor['selected_run_id'] if run_id is None else run_id
    if str(run_id) not in descriptor['runs']:
        raise ValueError('Requested run does not exist: {}'.format(run_id))
    run = descriptor['runs'][str(run_id)]
    candidates = [c for c in run['channels'] if c['source'] == 'model:standard_human'
                  and c['kind'] == trajectory_channel
                  and (sensor_group is None or c['sensor_group'] == sensor_group)]
    if len(candidates) != 1:
        raise ValueError('Select an unambiguous standard_human sensor group; found {}'.format(len(candidates)))
    selected = candidates[0]
    identity = {key: selected[key] for key in ('source', 'sensor_group', 'reference_frame')}
    if run['reference_frames'][identity['reference_frame']]['basis'] != 'blender_x_right_y_forward_z_up':
        raise ValueError('Unsupported coordinate basis; expected Blender X right, Y forward, Z up')
    model = run['models']['standard_human']
    if model['skeleton']['coordinate_system'] != 'blender':
        raise ValueError('Unsupported model coordinate system')
    kinds = [trajectory_channel] + (['SEGMENT_ORIGINS', 'ROTATIONS_WORLD'] if segments else [])
    if any(c['kind'] == 'DERIVED_POINTS' and all(c[k] == v for k, v in identity.items())
           for c in run['channels']):
        kinds.append('DERIVED_POINTS')
    arrays, frame_grid, times = {}, None, None
    for kind in kinds:
        channels = [c for c in run['channels'] if c['kind'] == kind and
                    all(c[key] == value for key, value in identity.items())]
        if len(channels) != 1:
            raise ValueError('Missing or ambiguous {} channel'.format(kind))
        channel = channels[0]
        components, unit = ('wxyz', '1') if kind == 'ROTATIONS_WORLD' else ('xyz', 'mm')
        if channel['components'] != dict.fromkeys(components, unit):
            raise ValueError('Unexpected components or units for {}'.format(kind))
        names = channel['names']
        if not names or len(names) != len(set(names)):
            raise ValueError('Empty or duplicate channel names')
        filters = [('run_id', '=', run_id), ('channel', '=', kind)]
        filters += [(key, '=', value) for key, value in identity.items()]
        columns = parquet.read_table(path, filters=filters, columns=[
            'frame_number', 'timestamp_s', 'name', 'component', 'value', 'units']).to_pydict()
        frames = sorted(set(columns['frame_number']))
        if not frames or any(not isinstance(f, int) for f in frames):
            raise ValueError('Missing or invalid frame numbers')
        values = np.full((len(frames), len(names), len(components)), np.nan)
        seen = np.zeros(values.shape, dtype=bool)
        timestamps = np.full(len(frames), np.nan)
        fi, ni = {f: i for i, f in enumerate(frames)}, {n: i for i, n in enumerate(names)}
        for frame, time, name, component, value, row_unit in zip(*(columns[c] for c in (
                'frame_number', 'timestamp_s', 'name', 'component', 'value', 'units'))):
            if name not in ni or component not in components or row_unit != unit or not np.isfinite(time):
                raise ValueError('Row conflicts with channel metadata')
            i, j, k = fi[frame], ni[name], components.index(component)
            if seen[i, j, k] or (np.isfinite(timestamps[i]) and timestamps[i] != time):
                raise ValueError('Duplicate component or conflicting timestamp')
            seen[i, j, k] = True
            timestamps[i] = time
            values[i, j, k] = np.nan if value is None else value
        if not seen.all() or np.isinf(values).any() or not (np.diff(timestamps) > 0).all():
            raise ValueError('Incomplete component grid, infinite values, or unordered timestamps')
        if frame_grid is not None and (frames != frame_grid or not np.array_equal(timestamps, times)):
            raise ValueError('Channels have different frame/timestamp grids')
        frame_grid, times = frames, timestamps
        if kind == 'ROTATIONS_WORLD':
            finite = np.isfinite(values).all(axis=2)
            if not np.allclose(np.linalg.norm(values[finite], axis=1), 1., atol=1e-4, rtol=0):
                raise ValueError('World rotations must be unit wxyz quaternions')
        else:
            values /= 1000.
        arrays[kind] = dict(zip(names, values.transpose(1, 0, 2)))
    expected = {l['name'] for l in model['skeleton']['landmarks']}
    if set(arrays[trajectory_channel]) != expected:
        raise ValueError('Trajectory names differ from the model snapshot')
    scales = None
    if segments:
        expected = {s['name'] for s in model['skeleton']['segments']}
        if any(set(arrays[k]) != expected for k in ('SEGMENT_ORIGINS', 'ROTATIONS_WORLD')):
            raise ValueError('Segment channels differ from the model snapshot')
        fits = [f for f in run['scale_fits'] if all(f[k] == v for k, v in identity.items())]
        if len(fits) != 1 or fits[0]['units'] != 'mm':
            raise ValueError('Missing or ambiguous segment scale fit in millimeters')
        scales = fits[0]['fit']['segment_scales']
        if any(s not in scales or not np.isfinite(scales[s]) or scales[s] <= 0 for s in expected):
            raise ValueError('Missing or invalid segment scales')
    return dict(path=str(path), run_id=run_id, **identity, frames=np.array(frame_grid),
                times=times, channels=arrays, model=model, scales=scales,
                camera_geometry=run.get('camera_geometry', {}).get(identity['sensor_group'], []),
                trajectory_channel=trajectory_channel)
