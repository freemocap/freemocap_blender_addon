"""Export a loaded Parquet scene without rewriting its source trajectories."""
from pathlib import Path

import bpy


def export(root, armature, formats, destination_folder, add_subfolder,
           bones_naming_convention, rest_pose_type, fbx_add_leaf_bones,
           fbx_primary_bone_axis, fbx_secondary_bone_axis):
    if bones_naming_convention != 'default' or rest_pose_type != 'default':
        raise ValueError('Parquet export currently preserves its Blender skeleton: choose default bone names and rest pose')
    if any(kind != 'fbx' for kind in formats):
        raise ValueError('Choose FBX for Parquet scenes; other format adapters are not implemented yet')
    mesh = next((o for o in armature.children if o.type == 'MESH' and 'skelly_mesh' in o.name), None)
    if mesh is None:
        raise ValueError('This model has no Skelly mesh to export')
    folder = Path(destination_folder) / '3d_models' if add_subfolder else Path(destination_folder)
    folder.mkdir(parents=True, exist_ok=True)
    selected = list(bpy.context.selected_objects)
    active = bpy.context.view_layer.objects.active
    frame = bpy.context.scene.frame_current
    hidden = {o: o.hide_get() for o in (armature, mesh)}
    try:
        bpy.ops.object.select_all(action='DESELECT')
        for obj in (armature, mesh):
            obj.hide_set(False)
            obj.select_set(True)
        bpy.context.view_layer.objects.active = armature
        bpy.ops.export_scene.fbx(
            filepath=str(folder / (root.name + '.fbx')), use_selection=True,
            object_types={'ARMATURE', 'MESH'}, bake_anim=True,
            bake_anim_use_all_bones=True, bake_anim_use_nla_strips=False,
            bake_anim_use_all_actions=False, bake_anim_force_startend_keying=True,
            use_mesh_modifiers=True, add_leaf_bones=fbx_add_leaf_bones,
            bake_anim_step=1., bake_anim_simplify_factor=0., armature_nodetype='NULL',
            primary_bone_axis=fbx_primary_bone_axis, secondary_bone_axis=fbx_secondary_bone_axis)
    finally:
        bpy.context.scene.frame_set(frame)
        bpy.ops.object.select_all(action='DESELECT')
        for obj, hide in hidden.items():
            obj.hide_set(hide)
        for obj in selected:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = active
