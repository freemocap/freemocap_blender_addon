"""Small adversarial recording fixtures; no producer package is imported."""
from copy import deepcopy
import importlib
import json

import bpy
import numpy as np


def run(package, output):
    dependencies = importlib.import_module(package + '.utilities.dependencies')
    arrow, parquet = dependencies.require_module('pyarrow'), dependencies.parquet_module()
    reader = importlib.import_module(package + '.freemocap_data_handler.parquet_recording')
    loader = importlib.import_module(package + '.core_functions.parquet_import')
    api = importlib.import_module(package + '.export_api')
    identity = dict(source='model:standard_human', sensor_group='test', reference_frame='world')
    model = dict(skeleton=dict(coordinate_system='blender',
        landmarks=[dict(name=n, segment=s, position=[0, .1, 0]) for n, s in [('a', 'root'), ('b', 'child')]],
        segments=[dict(name=s, landmarks=[n], frame=dict(primary_axis=[1, 1])) for n, s in [('a', 'root'), ('b', 'child')]]),
        rest_pose=dict(parents=dict(root=None, child='root')))
    channels = [dict(identity, kind=k, names=['a', 'b'] if k == 'LANDMARKS_3D' else ['root', 'child'],
                     components=dict.fromkeys('wxyz' if k == 'ROTATIONS_WORLD' else 'xyz', '1' if k == 'ROTATIONS_WORLD' else 'mm'))
                for k in ('LANDMARKS_3D', 'SEGMENT_ORIGINS', 'ROTATIONS_WORLD')]
    run = dict(channels=channels, reference_frames=dict(world=dict(basis='blender_x_right_y_forward_z_up')),
               models=dict(standard_human=model), scale_fits=[dict(identity, units='mm', fit=dict(segment_scales=dict(root=1000., child=1000.)))])
    descriptor = dict(schema_version=1, selected_run_id=4, runs={'4': run})
    rows = []
    for channel in channels:
        for frame in range(7, 10):
            for name in channel['names']:
                for component in channel['components']:
                    rotation = dict(zip('wxyz', [2 ** -.5, 0., 0., 2 ** -.5]))
                    value = rotation[component] if channel['kind'] == 'ROTATIONS_WORLD' else dict(x=1000., y=frame * 100., z=3000.)[component]
                    if frame == 9 and name in ('a', 'root'):
                        value = None
                    rows.append(dict(identity, channel=channel['kind'], frame_number=frame, timestamp_s=frame / 30.,
                                     name=name, component=component, value=value, units=channel['components'][component], run_id=4))
    path = output / 'contract_data.parquet'
    def write(meta=descriptor, values=rows):
        # Reverse rows to ensure import depends on keys, not physical ordering.
        table = arrow.Table.from_pylist(list(reversed(values)))
        parquet.write_table(table.replace_schema_metadata({b'freemocap.recording': json.dumps(meta).encode()}), path)
    write()
    data = reader.read_recording(path)
    np.testing.assert_allclose(data['channels']['LANDMARKS_3D']['b'][0], [1., .7, 3.])
    failures = []
    def rejects(label, meta=descriptor, values=rows, **kwargs):
        write(meta, values)
        try:
            reader.read_recording(path, **kwargs)
        except ValueError:
            failures.append(label)
        else:
            raise AssertionError('Accepted invalid contract: ' + label)
    rejects('unknown run', run_id=99)
    rejects('duplicate component', values=rows + [rows[0]])
    rejects('missing component', values=rows[1:])
    broken = deepcopy(descriptor)
    broken['schema_version'] = 999
    rejects('unknown schema', meta=broken)
    broken = deepcopy(descriptor)
    broken['runs']['4']['channels'][0]['components']['x'] = 'm'
    rejects('wrong units', meta=broken)
    broken = deepcopy(descriptor)
    broken['runs']['4']['reference_frames']['world']['basis'] = 'unknown'
    rejects('wrong basis', meta=broken)
    broken = deepcopy(descriptor)
    broken['runs']['4']['channels'].append(dict(channels[0], sensor_group='another'))
    rejects('ambiguous sensor group', meta=broken)
    write(broken)
    reader.read_recording(path, sensor_group='test')
    bad_rows = deepcopy(rows)
    next(r for r in bad_rows if r['channel'] == 'ROTATIONS_WORLD' and r['component'] == 'w')['value'] = 5.
    rejects('nonunit quaternion', values=bad_rows)
    bad_rows = deepcopy(rows)
    bad_rows[0]['timestamp_s'] += .001
    rejects('conflicting timestamp', values=bad_rows)
    # A fitted-skeleton source must never override the canonical model result.
    wrong_source = [dict(r, source='skeleton_fit:standard_human', value=999.) for r in rows]
    write(values=rows + wrong_source)
    scene = loader.load_parquet(path)
    bpy.context.scene.frame_set(9)
    assert not scene['segments']['child'].hide_viewport
    assert scene['segments']['root'].hide_viewport
    assert scene['rig'].pose.bones['child']['sample_valid']
    assert not scene['rig'].pose.bones['root']['sample_valid']
    # Exercise the real public export API, then reload its actual saved result.
    blend = output / 'contract-export.blend'
    api.export_recording(recording_path=path, blend_file_path=blend, route='parquet_segments')
    bpy.ops.wm.open_mainfile(filepath=str(blend))
    bpy.context.scene.frame_set(7)
    imported = [o for o in bpy.data.objects if o.get('import_route') == 'parquet_segments']
    assert len(imported) == 2
    assert all(o['run_id'] == 4 for o in imported)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    return dict(rejected=failures, explicit_sensor_selection=True, source_isolation=True,
                missing_parent_keeps_child=True, real_export_api=True)
