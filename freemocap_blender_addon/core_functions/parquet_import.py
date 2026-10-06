"""Two deliberately separate Blender skeleton builders for recording Parquet.

The native Blender skeleton displays independent measured segment poses. Its
bones are not connected/fitted; anatomical parents are retained as metadata.
The comparison skeleton uses the existing legacy armature and tracking constraints.
"""
import json

import bpy
import numpy as np
from mathutils import Quaternion, Vector

from ..freemocap_data_handler.parquet_recording import read_recording


def curves(obj):
    action = bpy.data.actions.new(obj.name + '_Action')
    obj.animation_data_create()
    obj.animation_data.action = action
    if bpy.app.version >= (4, 4):
        slot = action.slots.new(id_type='OBJECT', name=obj.name)
        strip = action.layers.new('Layer').strips.new(type='KEYFRAME')
        obj.animation_data.action_slot = slot
        return strip.channelbag(slot, ensure=True).fcurves
    return action.fcurves


def animate(fcurves, path, frames, values):
    values = np.asarray(values)
    if values.ndim == 1:
        values = values[:, None]
    for axis in range(values.shape[1]):
        curve = fcurves.new(data_path=path, index=axis)
        curve.keyframe_points.add(len(frames))
        curve.keyframe_points.foreach_set('co', np.column_stack((frames, values[:, axis])).ravel())
        # Samples are observations. Do not introduce Bezier overshoot or invented
        # intermediate rotations; validity changes take effect at the same frame.
        for key in curve.keyframe_points:
            key.interpolation = 'CONSTANT'
        curve.update()


def empty(name, parent=None):
    obj = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(obj)
    obj.parent = parent
    obj.empty_display_size = .015
    obj.empty_display_type = 'PLAIN_AXES'
    return obj


def trajectory(name, values, frames, parent, quaternion=None):
    obj = empty(name, parent)
    valid = np.isfinite(values).all(axis=1)
    if quaternion is not None:
        valid &= np.isfinite(quaternion).all(axis=1)
    obj['sample_valid'] = True
    fc = curves(obj)
    animate(fc, 'location', frames, np.where(valid[:, None], values, 0.))
    animate(fc, '["sample_valid"]', frames, valid.astype(float))
    animate(fc, 'hide_viewport', frames, (~valid).astype(float))
    animate(fc, 'hide_render', frames, (~valid).astype(float))
    if quaternion is not None:
        obj.rotation_mode = 'QUATERNION'
        animate(fc, 'rotation_quaternion', frames,
                np.where(valid[:, None], quaternion, [1., 0., 0., 0.]))
    return obj


def legacy_trajectories(data):
    """Explicit projection into the legacy rig vocabulary, never tracker identities.

    Keep canonical landmark centers. Only the legacy hand-midpoint helper has no
    canonical equivalent; retain the old index/pinky tip average for that target.
    """
    canonical = data['channels'][data['trajectory_channel']]
    result = dict(canonical)
    for landmark in data['model']['skeleton']['landmarks']:
        for alias in landmark.get('aliases', []):
            if alias not in canonical:
                result[alias] = canonical[landmark['name']]
    result['trunk_center'] = canonical['chest_center']
    for side in ('left', 'right'):
        for old, new in (('hip', 'hip_socket'), ('heel', 'calcaneus'),
                         ('foot_index', 'toe_tip'), ('hand_wrist', 'wrist'),
                         ('index', 'index_tip'), ('pinky', 'pinky_tip'), ('thumb', 'thumb_tip')):
            result[side + '_' + old] = canonical[side + '_' + new]
        for digit in ('thumb', 'index', 'middle', 'ring', 'pinky'):
            old_digit = digit + ('_finger' if digit in ('index', 'middle', 'ring') else '')
            for joint in ('cmc', 'mcp', 'ip', 'pip', 'dip', 'tip'):
                name = side + '_' + digit + '_' + joint
                if name in canonical:
                    result[side + '_hand_' + old_digit + '_' + joint] = canonical[name]
        result[side + '_hand_middle'] = (canonical[side + '_index_tip'] + canonical[side + '_pinky_tip']) / 2
    return result


def legacy_skeleton(data, root):
    from .create_rig.add_rig_bone_method import add_rig_by_bone
    from .create_rig.apply_bone_constraints import apply_bone_constraints
    from .empties.creation.create_empty_from_trajectory import create_keyframed_empty_from_3d_trajectory_data
    from ..data_models.bones.bone_definitions import get_bone_definitions
    from ..data_models.bones.bone_constraints import get_bone_constraint_definitions
    values = legacy_trajectories(data)
    definitions, constraints = get_bone_definitions(), get_bone_constraint_definitions()
    required = {n for b in definitions.values() for n in (b.head, b.tail)}
    required |= {c.target for cs in constraints.values() for c in cs if hasattr(c, 'target')}
    missing = required - values.keys()
    if missing:
        raise ValueError('Missing legacy constraint targets: ' + ', '.join(sorted(missing)))
    bone_data = {}
    for name, definition in definitions.items():
        lengths = np.linalg.norm(values[definition.tail] - values[definition.head], axis=1)
        finite = lengths[np.isfinite(lengths)]
        bone_data[name] = {'median': float(np.median(finite)) if len(finite) else float('nan')}
    targets_parent = empty('legacy_constraint_targets', root)
    targets = {}
    for name in sorted(required):
        # Match the old display treatment of missing observations (hold/backfill).
        # Canonical landmark objects remain separate and retain their validity.
        targets[name] = create_keyframed_empty_from_3d_trajectory_data(
            values[name], 'legacy_' + name, parent_object=targets_parent, empty_scale=.01)
    rig = add_rig_by_bone(bone_data, 'Legacy Blender skeleton')
    rig.parent = root
    apply_bone_constraints(rig=rig, add_fingers_constraints=True, parent_object=root,
                           bone_constraint_definitions=constraints, target_objects=targets)
    bpy.ops.object.mode_set(mode='OBJECT')
    rig['reconstruction'] = 'legacy Blender constraints; fixed median lengths; missing targets held/backfilled'
    return rig, targets


def native_skeleton(data, root):
    frames = data['frames']
    origins, rotations = (data['channels'][k] for k in ('SEGMENT_ORIGINS', 'ROTATIONS_WORLD'))
    segment_parent = empty('segments', root)
    segment_objects = {n: trajectory(n, origins[n], frames, segment_parent, rotations[n]) for n in origins}
    armature = bpy.data.armatures.new('SkellyForge segment display')
    rig = bpy.data.objects.new('Blender skeleton', armature)
    bpy.context.collection.objects.link(rig)
    rig.parent = root
    bpy.ops.object.select_all(action='DESELECT')
    rig.select_set(True)
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode='EDIT')
    landmarks = {l['name']: l for l in data['model']['skeleton']['landmarks']}
    for segment in data['model']['skeleton']['segments']:
        name, frame = segment['name'], segment['frame']
        bone = armature.edit_bones.new(name)
        # Drawing direction follows the authored primary axis, not an estimated
        # direction between animated landmarks. Translation stays at segment origin.
        axis, sign = frame['primary_axis']
        direction = Vector((0., 0., 0.))
        direction[axis] = sign
        local = [Vector(landmarks[n]['position']).length for n in segment['landmarks']
                 if landmarks[n]['segment'] == name]
        length = max(local, default=0.) * data['scales'][name] / 1000.
        bone.head = (0., 0., 0.)
        bone.tail = direction * max(length, .005)
    bpy.ops.object.mode_set(mode='OBJECT')
    fc = curves(rig)
    for name in origins:
        bone = rig.pose.bones[name]
        basis = bone.bone.matrix_local.to_quaternion()
        inverse = basis.conjugated()
        valid = np.isfinite(origins[name]).all(axis=1) & np.isfinite(rotations[name]).all(axis=1)
        positions = [inverse @ Vector(v) if good else Vector((0., 0., 0.))
                     for v, good in zip(origins[name], valid)]
        quaternions = [inverse @ Quaternion(q) @ basis if good else Quaternion()
                       for q, good in zip(rotations[name], valid)]
        bone.rotation_mode = 'QUATERNION'
        bone['anatomical_parent'] = data['model']['rest_pose']['parents'].get(name) or ''
        bone['sample_valid'] = True
        for prop, values in [('location', positions), ('rotation_quaternion', quaternions),
                             ('scale', np.repeat(valid[:, None], 3, axis=1)),
                             ('["sample_valid"]', valid.astype(float))]:
            path = bone.path_from_id() + (prop if prop.startswith('[') else '.' + prop)
            animate(fc, path, frames, values)
    rig['reconstruction'] = 'saved independent segment world poses; no connected skeleton fit'
    return rig, segment_objects


def load_parquet(path, *, route='parquet_segments', trajectory_channel='LANDMARKS_3D',
                 run_id=None, sensor_group=None):
    if route not in ('parquet_segments', 'parquet_constraints'):
        raise ValueError('Unknown Parquet import route: ' + route)
    native = route == 'parquet_segments'
    if native and trajectory_channel != 'LANDMARKS_3D':
        raise ValueError('Saved segment poses must use model landmarks')
    data = read_recording(path, trajectory_channel=trajectory_channel, segments=native,
                          run_id=run_id, sensor_group=sensor_group)
    frames = data['frames']
    if not np.array_equal(frames, np.arange(frames[0], frames[0] + len(frames))) or frames[0] < 0:
        raise ValueError('This loader requires contiguous, nonnegative source frame numbers')
    if bpy.context.object is not None and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    previous_objects = set(bpy.data.objects)
    scene = bpy.context.scene
    scene.frame_start, scene.frame_end = int(frames[0]), int(frames[-1])
    if len(frames) > 1:
        fps = float(1. / np.median(np.diff(data['times'])))
        scene.render.fps = max(1, round(fps))
        scene.render.fps_base = scene.render.fps / fps
    try:
        root = empty('FreeMoCap_' + route)
        root['import_route'] = route
        root['trajectory_channel'] = trajectory_channel
        root['recording_path'] = data['path']
        root['run_id'] = data['run_id']
        root['sensor_group'] = data['sensor_group']
        root['source'] = data['source']
        root['timestamps_s'] = json.dumps(data['times'].tolist())
        root['model_snapshot'] = json.dumps(data['model'])
        parent = empty('landmarks_empties_parent' if trajectory_channel == 'LANDMARKS_3D' else 'mapped_keypoints_empties_parent', root)
        landmarks = {n: trajectory(n, v, frames, parent) for n, v in data['channels'][trajectory_channel].items()}
        rig, objects = native_skeleton(data, root) if native else legacy_skeleton(data, root)
        scene.frame_set(int(frames[0]))
        result = dict(root=root, rig=rig, landmarks=landmarks,
                      segments=objects if native else {}, targets={} if native else objects, data=data)
        from .parquet_scene import build_scene
        build_scene(result)
        scene.frame_set(int(frames[0]))
        return result
    except Exception:
        if bpy.context.object is not None and bpy.context.object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        for obj in set(bpy.data.objects) - previous_objects:
            bpy.data.objects.remove(obj, do_unlink=True)
        raise
