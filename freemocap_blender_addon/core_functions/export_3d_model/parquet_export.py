"""Export a loaded Parquet scene without rewriting its source trajectories."""
from pathlib import Path
from contextlib import contextmanager
import json

import bpy

from ...utilities.get_fcurves_from_object_action import get_fcurves_from_object_action


@contextmanager
def bvh_armature(root, armature, path):
    """BVH has no scale/visibility channel; isolate native missing-sample display."""
    if root.get('import_route') != 'parquet_segments':
        yield armature
        return
    copy = armature.copy()
    copy.data = armature.data.copy()
    action = None
    data = copy.data
    try:
        bpy.context.collection.objects.link(copy)
        if armature.animation_data and armature.animation_data.action:
            action = armature.animation_data.action.copy()
            copy.animation_data.action = action
        curves = get_fcurves_from_object_action(copy)
        missing = {}
        if curves is not None:
            for bone in copy.pose.bones:
                validity = bone.path_from_id() + '["sample_valid"]'
                curve = next((c for c in curves if c.data_path == validity), None)
                if curve is not None:
                    missing[bone.name] = [frame for frame in range(bpy.context.scene.frame_start,
                        bpy.context.scene.frame_end + 1) if curve.evaluate(frame) < .5]
            for curve in list(curves):
                if curve.data_path.endswith('.scale'):
                    curves.remove(curve)
        for bone in copy.pose.bones:
            bone.scale = (1., 1., 1.)
        copy.hide_set(False)
        copy.select_set(True)
        bpy.context.view_layer.objects.active = copy
        bpy.context.view_layer.update()
        yield copy
        path.with_suffix('.bvh.metadata.json').write_text(json.dumps(dict(
            import_route='parquet_segments', run_id=root.get('run_id'),
            sensor_group=root.get('sensor_group'), source=root.get('source'),
            missing_sample_policy='Existing zero-location/identity-rotation placeholders; visibility is not encoded in BVH',
            missing_frames_by_bone=missing), indent=2), encoding='utf-8')
    finally:
        bpy.data.objects.remove(copy, do_unlink=True)
        bpy.data.armatures.remove(data)
        if action is not None:
            bpy.data.actions.remove(action)
        bpy.context.view_layer.objects.active = armature


def export(root, armature, formats, destination_folder, add_subfolder,
           bones_naming_convention, rest_pose_type, fbx_add_leaf_bones,
           fbx_primary_bone_axis, fbx_secondary_bone_axis):
    if bones_naming_convention != 'default' or rest_pose_type != 'default':
        raise ValueError('Parquet export currently preserves its Blender skeleton: choose default bone names and rest pose')
    if any(kind not in ('fbx', 'bvh') for kind in formats):
        raise ValueError('Parquet scenes support FBX and BVH export through Blender')
    mesh = next((o for o in armature.children if o.type == 'MESH' and 'skelly_mesh' in o.name), None)
    if 'fbx' in formats and mesh is None:
        raise ValueError('This model has no Skelly mesh to export')
    folder = Path(destination_folder) / '3d_models' if add_subfolder else Path(destination_folder)
    folder.mkdir(parents=True, exist_ok=True)
    selected = list(bpy.context.selected_objects)
    active = bpy.context.view_layer.objects.active
    frame = bpy.context.scene.frame_current
    objects = [armature] + ([mesh] if mesh is not None and 'fbx' in formats else [])
    hidden = {o: o.hide_get() for o in objects}
    try:
        bpy.ops.object.select_all(action='DESELECT')
        for obj in objects:
            obj.hide_set(False)
            obj.select_set(True)
        bpy.context.view_layer.objects.active = armature
        for kind in formats:
            if kind == 'fbx':
                outcome = bpy.ops.export_scene.fbx(
                    filepath=str(folder / (root.name + '.fbx')), use_selection=True,
                    object_types={'ARMATURE', 'MESH'}, bake_anim=True,
                    bake_anim_use_all_bones=True, bake_anim_use_nla_strips=False,
                    bake_anim_use_all_actions=False, bake_anim_force_startend_keying=True,
                    use_mesh_modifiers=True, add_leaf_bones=fbx_add_leaf_bones,
                    bake_anim_step=1., bake_anim_simplify_factor=0., armature_nodetype='NULL',
                    primary_bone_axis=fbx_primary_bone_axis, secondary_bone_axis=fbx_secondary_bone_axis)
            else:
                # Blender evaluates the loaded rig, including constraints. Keep
                # non-root translations, as in the legacy Blender export path.
                path = folder / (root.name + '.bvh')
                with bvh_armature(root, armature, path):
                    outcome = bpy.ops.export_anim.bvh(
                        filepath=str(path),
                        frame_start=bpy.context.scene.frame_start,
                        frame_end=bpy.context.scene.frame_end,
                        root_transform_only=False, global_scale=1.0)
                    if outcome != {'FINISHED'}:
                        raise RuntimeError('Blender did not finish BVH export')
            if outcome != {'FINISHED'}:
                raise RuntimeError('Blender did not finish ' + kind.upper() + ' export')
    finally:
        bpy.context.scene.frame_set(frame)
        bpy.ops.object.select_all(action='DESELECT')
        for obj, hide in hidden.items():
            obj.hide_set(hide)
        for obj in selected:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = active
