"""Installed-package acceptance checks, run inside each supported Blender ABI."""
import importlib
import json
import os
from pathlib import Path

import bpy
import numpy as np
from mathutils import Quaternion, Vector
spec = importlib.util.spec_from_file_location('complete_scene', Path(__file__).with_name('blender_complete_scene_checks.py'))
complete_scene = importlib.util.module_from_spec(spec)
spec.loader.exec_module(complete_scene)


def check_native(result, frames):
    data = result['data']
    rig = bpy.data.objects[result['rig_name']]
    assert not any(b.constraints for b in rig.pose.bones)
    assert len(rig.pose.bones) == len(data['channels']['SEGMENT_ORIGINS'])
    for i in frames:
        bpy.context.scene.frame_set(int(data['frames'][i]))
        depsgraph = bpy.context.evaluated_depsgraph_get()
        evaluated = rig.evaluated_get(depsgraph)
        for name, values in data['channels']['LANDMARKS_3D'].items():
            obj = bpy.data.objects[result['landmark_names'][name]]
            valid = bool(np.isfinite(values[i]).all())
            assert bool(obj['sample_valid']) == valid
            assert obj.hide_viewport != valid
            if valid:
                np.testing.assert_allclose(list(obj.matrix_world.translation), values[i], atol=2e-6, rtol=0)
        for name, values in data['channels']['SEGMENT_ORIGINS'].items():
            q = data['channels']['ROTATIONS_WORLD'][name][i]
            valid = bool(np.isfinite(values[i]).all() and np.isfinite(q).all())
            obj = bpy.data.objects[result['segment_names'][name]]
            bone = evaluated.pose.bones[name]
            assert bool(obj['sample_valid']) == valid
            assert bool(bone['sample_valid']) == valid
            if valid:
                np.testing.assert_allclose(list(obj.matrix_world.translation), values[i], atol=2e-6, rtol=0)
                np.testing.assert_allclose(np.array(obj.matrix_world.to_3x3()), np.array(Quaternion(q).to_matrix()), atol=2e-5, rtol=0)
                np.testing.assert_allclose(list(bone.matrix.translation), values[i], atol=2e-6, rtol=0)
                # Remove the fixed Blender bone drawing basis to recover the
                # segment's exact world orientation (not an endpoint estimate).
                actual = bone.matrix.to_3x3() @ bone.bone.matrix_local.to_3x3().inverted()
                np.testing.assert_allclose(np.array(actual), np.array(Quaternion(q).to_matrix()), atol=2e-5, rtol=0)
            else:
                assert max(abs(v) for v in bone.scale) == 0


def build_checks(package, output):
    manifest = os.environ.get('FREEMOCAP_BLENDER_REFERENCE_MANIFEST')
    references = json.loads(Path(manifest).read_text(encoding='utf-8')) if manifest else []
    loader = importlib.import_module(package + '.core_functions.parquet_import')
    definitions = importlib.import_module(package + '.data_models.bones.bone_constraints')
    api = importlib.import_module(package + '.export_api')
    attachment = importlib.import_module(package + '.core_functions.meshes.skelly_mesh.attachment_frame')
    # Analytic cases include an antiparallel primary (the former upside-down
    # head failure), and a rotated rest frame. Up must remain fully specified.
    identity = Quaternion((1, 0, 0, 0))
    for source, expected in (((0, 1, 0), np.eye(3)),
                             ((0, -1, 0), np.diag([-1., -1., 1.]))):
        rotation = attachment.attachment_rotation(source, (0, 1, 0), identity, (0, 0, 1))
        np.testing.assert_allclose(rotation, expected, atol=1e-6)
        np.testing.assert_allclose(rotation @ Vector((0, 0, 1)), (0, 0, 1), atol=1e-6)
    quarter_turn = Quaternion((0, 0, 1), np.pi / 2)
    rotation = attachment.attachment_rotation((0, 1, 0), (0, 1, 0), quarter_turn, (0, 0, 1))
    np.testing.assert_allclose(rotation, np.eye(3), atol=1e-6)
    # An explicitly defined skull-up landmark takes precedence over a rolled
    # authored rest pose. Binding must remain +Y nose/+Z up in segment space.
    rolled_rest = Quaternion((0, 1, 0), np.pi / 2)
    rotation = attachment.attachment_rotation((0, 1, 0), (0, 1, 0), rolled_rest,
                                               (0, 0, 1), local_secondary=(0, 0, 1))
    np.testing.assert_allclose(rotation, np.eye(3), atol=1e-6)
    try:
        attachment.basis((0, 0, 1), (0, 0, 1))
        raise AssertionError('Parallel frame accepted')
    except ValueError:
        pass
    reports = []
    for reference in references:
        native = loader.load_parquet(reference['path'])
        complete_scene.check_anatomy(native, Path(importlib.import_module(package).__file__).parent)
        data = native['data']
        native_scene = complete_scene.check(native, reference)
        if os.environ.get('FREEMOCAP_TEST_RENDER') == '1':
            complete_scene.render_preview(native, output / (reference['dataset'] + '-native.png'))
        assert len(data['frames']) == reference['frames']
        state = dict(data=data, rig_name=native['rig'].name,
                     landmark_names={n: o.name for n, o in native['landmarks'].items()},
                     segment_names={n: o.name for n, o in native['segments'].items()})
        check_native(state, range(len(data['frames'])))
        legacy = loader.load_parquet(reference['path'], route='parquet_constraints')
        legacy_scene = complete_scene.check(legacy, reference)
        if os.environ.get('FREEMOCAP_TEST_RENDER') == '1':
            complete_scene.render_preview(legacy, output / (reference['dataset'] + '-constraints.png'))
        if reference['dataset'] == 'test_data':
            export = importlib.import_module(package + '.core_functions.export_3d_model.export_3d_model').export_3d_model
            for result in (native, legacy):
                scene = bpy.context.scene
                frame = scene.frame_current
                landmark = result['landmarks']['pelvis_origin']
                position = landmark.matrix_world.copy()
                export(result['root'], result['rig'], formats=['fbx'], destination_folder=str(output))
                assert (output / (result['root'].name + '.fbx')).stat().st_size > 10000
                assert scene.frame_current == frame
                np.testing.assert_allclose(np.array(landmark.matrix_world), np.array(position), atol=1e-6)
        rig = legacy['rig']
        # All expected active constraints must exist, with exact scoped targets.
        expected_count = 0
        for name, cs in definitions.get_bone_constraint_definitions().items():
            if name not in rig.pose.bones:
                continue
            expected = [c for c in cs if c.type != definitions.ConstraintType.LIMIT_ROTATION]
            actual = list(rig.pose.bones[name].constraints)
            assert len(actual) == len(expected), name
            expected_count += len(expected)
            for a, e in zip(actual, expected):
                assert a.type == e.type.value
                if hasattr(e, 'target'):
                    assert a.target == legacy['targets'][e.target]
        assert expected_count > 50
        # Compare corresponding segment origins / legacy bone heads. They need
        # not be equal: the old connected, median-length rig solves differently.
        pairs = [('left_upper_arm', 'upper_arm.L'), ('right_upper_arm', 'upper_arm.R'),
                 ('left_lower_arm', 'forearm.L'), ('right_lower_arm', 'forearm.R'),
                 ('left_lower_leg', 'shin.L'), ('right_lower_leg', 'shin.R')]
        errors = []
        for i, frame in enumerate(data['frames']):
            bpy.context.scene.frame_set(int(frame))
            evaluated = rig.evaluated_get(bpy.context.evaluated_depsgraph_get())
            for segment, bone in pairs:
                position = np.array(evaluated.pose.bones[bone].matrix.translation)
                assert np.isfinite(position).all()
                origin = data['channels']['SEGMENT_ORIGINS'][segment][i]
                if np.isfinite(origin).all():
                    errors.append(float(np.linalg.norm(position - origin)))
        # Prove this route really follows the targets and is not a pose replay.
        frame = int(data['frames'][len(data['frames']) // 2])
        bpy.context.scene.frame_set(frame)
        before = np.array(rig.evaluated_get(bpy.context.evaluated_depsgraph_get()).pose.bones['pelvis'].matrix.translation)
        target = legacy['targets']['hips_center']
        target.delta_location.x = .25
        bpy.context.view_layer.update()
        after = np.array(rig.evaluated_get(bpy.context.evaluated_depsgraph_get()).pose.bones['pelvis'].matrix.translation)
        np.testing.assert_allclose(after - before, [.25, 0, 0], atol=2e-5, rtol=0)
        target.delta_location.x = 0
        bpy.context.view_layer.update()
        legacy_name = rig.name
        scene_file = output / (reference['dataset'] + '-both-routes.blend')
        bpy.ops.wm.save_as_mainfile(filepath=str(scene_file))
        bpy.ops.wm.open_mainfile(filepath=str(scene_file))
        complete_scene.check_reopened(native_scene)
        complete_scene.check_reopened(legacy_scene)
        check_native(state, sorted(set([0, len(data['frames']) // 2, len(data['frames']) - 1])))
        assert sum(len(b.constraints) for b in bpy.data.objects[legacy_name].pose.bones) == expected_count
        reports.append(dict(dataset=reference['dataset'], frames=len(data['frames']),
                            landmarks=len(state['landmark_names']), segments=len(state['segment_names']),
                            native_all_frames=True, legacy_constraints=expected_count,
                            native_scene=native_scene, legacy_scene=legacy_scene,
                            legacy_target_response=True, save_reopen=True, full_loader_tested=True,
                            comparison_head_distance_median_m=float(np.median(errors)),
                            comparison_head_distance_max_m=float(np.max(errors)), scene=str(scene_file)))
        # Keep the next dataset's saved comparison scene self-contained.
        for obj in list(bpy.data.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        # The optional comparison input must stay mapped observations rather
        # than silently selecting rigidified landmarks or saved segment poses.
        mapped = loader.load_parquet(reference['path'], route='parquet_constraints',
                                     trajectory_channel='MAPPED_KEYPOINTS_3D')
        assert set(mapped['data']['channels']) == {'MAPPED_KEYPOINTS_3D', 'DERIVED_POINTS'}
        values = mapped['data']['channels']['MAPPED_KEYPOINTS_3D']['pelvis_origin']
        for i in np.flatnonzero(np.isfinite(values).all(axis=1)):
            bpy.context.scene.frame_set(int(mapped['data']['frames'][i]))
            np.testing.assert_allclose(list(mapped['landmarks']['pelvis_origin'].matrix_world.translation),
                                       values[i], atol=2e-6, rtol=0)
        assert any(not np.allclose(v, data['channels']['LANDMARKS_3D'][n], equal_nan=True)
                   for n, v in mapped['data']['channels']['MAPPED_KEYPOINTS_3D'].items())
        assert sum(len(b.constraints) for b in mapped['rig'].pose.bones) == expected_count
        for obj in list(bpy.data.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        # Exercise the actual standalone Load Data operator, not just its helper.
        props = bpy.context.scene.freemocap_properties
        props.recording_path = str(Path(reference['path']).parent)
        props.import_route = 'parquet_constraints'
        props.trajectory_channel = 'LANDMARKS_3D'
        assert bpy.ops.freemocap._load_data() == {'FINISHED'}
        assert any(o.get('import_route') == 'parquet_constraints' for o in bpy.data.objects)
        for obj in list(bpy.data.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        reports[-1].update(mapped_observations_checked=True, standalone_operator=True)
    return reports
