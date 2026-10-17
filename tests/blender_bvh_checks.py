"""Consumer checks for Blender-written BVH, shared by real recording tests."""
from pathlib import Path
import json

import bpy
import numpy as np


def check_roundtrip(armature, path, frames):
    scene = bpy.context.scene
    original_frame = scene.frame_current
    expected = {}
    for frame in frames:
        scene.frame_set(frame)
        evaluated = armature.evaluated_get(bpy.context.evaluated_depsgraph_get())
        expected[frame] = {
            bone.name: (np.array(bone.head),
                        np.array((bone.matrix @ bone.bone.matrix_local.inverted()).to_quaternion().to_matrix()))
            for bone in evaluated.pose.bones if min(abs(v) for v in bone.scale) > 1e-6
        }
    text = Path(path).read_text()
    assert 'Frames: %d' % (scene.frame_end - scene.frame_start + 1) in text
    frame_time = float(text.split('Frame Time:')[1].splitlines()[0])
    assert abs(frame_time - scene.render.fps_base / scene.render.fps) < 1e-6
    before = set(bpy.data.objects)
    try:
        # Blender's BVH importer clamps start frames below one. BVH stores
        # relative sample time, so compare with an explicit origin mapping.
        source_start = scene.frame_start
        assert bpy.ops.import_anim.bvh(filepath=str(path), frame_start=1,
            axis_forward='Y', axis_up='Z', use_fps_scale=False,
            update_scene_fps=False, update_scene_duration=False) == {'FINISHED'}
        imported = bpy.context.object
        assert set(armature.pose.bones.keys()).issubset(imported.pose.bones.keys())
        for name, bone in armature.data.bones.items():
            if bone.parent:
                assert imported.data.bones[name].parent.name == bone.parent.name
        for frame, bones in expected.items():
            scene.frame_set(1 + frame - source_start)
            evaluated = imported.evaluated_get(bpy.context.evaluated_depsgraph_get())
            for name, (position, rotation) in bones.items():
                bone = evaluated.pose.bones[name]
                np.testing.assert_allclose(np.array(bone.head), position, atol=2e-5, rtol=0,
                    err_msg=f'BVH position: {name}, frame {frame}')
                actual = (bone.matrix @ bone.bone.matrix_local.inverted()).to_quaternion().to_matrix()
                np.testing.assert_allclose(np.array(actual), rotation, atol=2e-4, rtol=0,
                    err_msg=f'BVH rotation: {name}, frame {frame}')
    finally:
        for obj in set(bpy.data.objects) - before:
            bpy.data.objects.remove(obj, do_unlink=True)
        scene.frame_set(original_frame)


def check_export(export, result, output):
    scene = bpy.context.scene
    frame = scene.frame_current
    selected = set(bpy.context.selected_objects)
    active = bpy.context.view_layer.objects.active
    objects = set(bpy.data.objects)
    actions = set(bpy.data.actions)
    scales = {bone.name: tuple(bone.scale) for bone in result['rig'].pose.bones}
    export(result['root'], result['rig'], formats=['bvh'], destination_folder=str(output))
    assert scene.frame_current == frame
    assert set(bpy.context.selected_objects) == selected
    assert bpy.context.view_layer.objects.active == active
    assert set(bpy.data.objects) == objects
    assert set(bpy.data.actions) == actions
    assert {bone.name: tuple(bone.scale) for bone in result['rig'].pose.bones} == scales
    path = Path(output) / (result['root'].name + '.bvh')
    if result['root']['import_route'] == 'parquet_segments':
        metadata = json.loads(path.with_suffix('.bvh.metadata.json').read_text())
        for name, values in result['data']['channels']['SEGMENT_ORIGINS'].items():
            rotations = result['data']['channels']['ROTATIONS_WORLD'][name]
            invalid = ~(np.isfinite(values).all(axis=1) & np.isfinite(rotations).all(axis=1))
            assert metadata['missing_frames_by_bone'][name] == result['data']['frames'][invalid].tolist()
    frames = sorted(set(np.linspace(scene.frame_start, scene.frame_end, 7, dtype=int).tolist()))
    check_roundtrip(result['rig'], path, frames)
