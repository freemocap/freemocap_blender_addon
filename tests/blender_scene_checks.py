"""Blender-only tests of real animation evaluation; no producer imports.

The reference-data adapter below is a test fixture, NOT the future production
Parquet loader. It checks bundled PyArrow against core's real output, and a
representative saved trajectory against the existing Blender animation primitive.
"""
import importlib
import json
import os
from pathlib import Path

import bpy
import numpy as np


def assert_locations(checks):
    for check in checks:
        obj = bpy.data.objects[check['name']]
        for frame, expected in check['samples']:
            bpy.context.scene.frame_set(frame)
            actual = obj.evaluated_get(bpy.context.evaluated_depsgraph_get()).matrix_world.translation
            np.testing.assert_allclose(list(actual), expected, rtol=0, atol=1e-5)


def build_checks(package, parquet, include_references):
    create = importlib.import_module(package + '.core_functions.empties.creation.create_empty_from_trajectory').create_keyframed_empty_from_3d_trajectory_data
    bpy.context.scene.frame_start = 7
    values = np.array([[1., 2., 3.], [2., 4., 6.], [3., 6., 9.]])
    obj = create(values, 'test_synthetic_trajectory')
    checks = [dict(name=obj.name, samples=[[7 + i, row.tolist()] for i, row in enumerate(values)])]
    missing = create(np.array([[np.nan, 1., np.nan], [2., np.nan, np.nan], [4., 3., np.nan]]), 'test_missing_trajectory')
    checks.append(dict(name=missing.name, samples=[[7, [2., 1., 0.]], [8, [2., 1., 0.]], [9, [4., 3., 0.]]]))
    reports = []
    manifest = os.environ.get('FREEMOCAP_BLENDER_REFERENCE_MANIFEST')
    references = json.loads(Path(manifest).read_text(encoding='utf-8')) if manifest and include_references else []
    for reference in references:
        with parquet.ParquetFile(reference['path']) as reader:
            descriptor = json.loads(reader.schema_arrow.metadata[b'freemocap.recording'])
        assert descriptor['schema_version'] == 1
        run_id = descriptor['selected_run_id'] if reference['run_id'] is None else reference['run_id']
        run = descriptor['runs'][str(run_id)]
        channels = [c for c in run['channels'] if c['kind'] == 'LANDMARKS_3D' and c['source'] == 'model:standard_human'
                    and (reference['sensor_group'] is None or c['sensor_group'] == reference['sensor_group'])]
        assert len(channels) == 1, 'Reference needs an explicit, unambiguous sensor group'
        channel = channels[0]
        assert channel['components'] == dict.fromkeys('xyz', 'mm')
        assert run['reference_frames'][channel['reference_frame']]['basis'] == 'blender_x_right_y_forward_z_up'
        name = 'pelvis_origin' if 'pelvis_origin' in channel['names'] else channel['names'][0]
        filters = [('run_id', '=', run_id), ('channel', '=', 'LANDMARKS_3D'), ('name', '=', name)]
        filters += [(key, '=', channel[key]) for key in ('source', 'sensor_group', 'reference_frame')]
        rows = parquet.read_table(reference['path'], filters=filters,
                                  columns=['frame_number', 'timestamp_s', 'component', 'value', 'units']).to_pylist()
        frames = {}
        for row in rows:
            assert row['units'] == 'mm' and row['component'] in 'xyz'
            frame = frames.setdefault(row['frame_number'], dict(time=row['timestamp_s'], values={}))
            assert frame['time'] == row['timestamp_s']
            assert row['component'] not in frame['values'], 'Duplicate frame/component'
            frame['values'][row['component']] = row['value']
        indices = sorted(frames)
        assert len(indices) == reference['frames']
        assert indices == list(range(indices[0], indices[0] + len(indices))), 'Noncontiguous frames need a dedicated loader'
        times = np.array([frames[i]['time'] for i in indices])
        assert np.isfinite(times).all() and (np.diff(times) > 0).all()
        assert all(set(frames[i]['values']) == set('xyz') for i in indices)
        values = np.array([[frames[i]['values'][c] for c in 'xyz'] for i in indices], dtype=float) / 1000.
        finite = np.isfinite(values).all(axis=1)
        assert finite.any(), 'No finite positions in the selected reference trajectory'
        bpy.context.scene.frame_start = indices[0]
        obj = create(values, 'test_' + reference['dataset'] + '_' + name)
        checks.append(dict(name=obj.name, samples=[[i, values[k].tolist()] for k, i in enumerate(indices) if finite[k]]))
        available = {c['kind'] for c in run['channels'] if all(c[key] == channel[key] for key in ('source', 'sensor_group', 'reference_frame'))}
        missing_channels = sorted({'MAPPED_KEYPOINTS_3D', 'LANDMARKS_3D', 'SEGMENT_ORIGINS', 'ROTATIONS_WORLD'} - available)
        reports.append(dict(dataset=reference['dataset'], run_id=run_id, sensor_group=channel['sensor_group'],
                            source=channel['source'], trajectory=name, frames=len(indices),
                            finite_frames=int(finite.sum()), sha256=reference['sha256'],
                            missing_new_pipeline_channels=missing_channels, full_loader_tested=False))
    assert_locations(checks)
    return checks, reports
