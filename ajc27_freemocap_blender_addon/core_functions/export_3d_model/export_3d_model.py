import os

import bpy

from ajc27_freemocap_blender_addon.core_functions.export_3d_model.helpers.bone_naming_mapping import (
    bone_naming_mapping,
)
from ajc27_freemocap_blender_addon.core_functions.export_3d_model.helpers.restore_daz_g8_1 import (
    restore_daz_g8_1_edit_mode,
    restore_daz_g8_1_pose_mode,
)
from ajc27_freemocap_blender_addon.core_functions.export_3d_model.helpers.restore_metahuman import (
    restore_metahuman_edit_mode,
    restore_metahuman_pose_mode,
)
from ajc27_freemocap_blender_addon.core_functions.export_3d_model.helpers.set_armature_pose_by_markers import (
    set_armature_pose_by_markers,
)
from ajc27_freemocap_blender_addon.core_functions.export_3d_model.helpers.set_armature_rest_pose import (
    set_armature_rest_pose,
)
from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.helpers.mesh_utilities import (
    get_bone_info,
)
from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.helpers.skelly_vertex_groups import (
    _SKELLY_VERTEX_GROUPS,
)
from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.strategies.attach_skelly_by_vertex_groups import (
    align_and_parent_vertex_groups_to_armature,
)


def export_3d_model(
    data_parent_empty: bpy.types.Object,
    armature: bpy.types.Armature,
    formats: list = None,
    destination_folder: str = '',
    add_subfolder: bool = False,
    rename_root_bone: bool = False,
    bones_naming_convention: str = 'default',
    rest_pose_type: str = 'default',
    restore_defaults_after_export: bool = True,
    fbx_add_leaf_bones: bool = True,
    fbx_primary_bone_axis: str = 'Y',
    fbx_secondary_bone_axis: str = 'X',
) -> None:
    if formats is None:
        formats = ['fbx', 'bvh']

    # 1. Setup and Preparation
    _prepare_scene()
    export_folder = _get_export_folder(destination_folder, add_subfolder)
    mesh_object = [
        obj for obj in data_parent_empty.children_recursive
        if 'skelly_mesh' in obj.name
    ][0]
    empties_parent = [
        obj for obj in data_parent_empty.children
        if 'empties_parent' in obj.name
    ][0]

    # 2. Save Current State
    armature_original_name = armature.name
    current_bone_info = {}
    if rest_pose_type != 'default':
        current_bone_info = get_bone_info(armature)

    current_markers_position = {
        marker.name: marker.matrix_world.translation.copy()
        for marker in empties_parent.children
    }

    # 3. Apply Export Configurations
    if rename_root_bone and armature.name != "root":
        armature.name = "root"

    if rest_pose_type != 'default':
        set_armature_rest_pose(
            data_parent_empty=data_parent_empty,
            armature=armature,
            rest_pose_type=rest_pose_type
        )
        align_and_parent_vertex_groups_to_armature(
            armature=armature,
            mesh_object=mesh_object,
            vertex_groups=_SKELLY_VERTEX_GROUPS
        )

    set_armature_pose_by_markers(
        data_parent_empty=data_parent_empty,
        armature=armature
    )

    if bones_naming_convention != "default":
        _apply_bone_naming(armature, bones_naming_convention)

    # 4. Perform Format Exports
    export_file_base = data_parent_empty.name.removesuffix("_origin")
    for export_format in formats:
        export_path = os.path.join(
            export_folder, f"{export_file_base}.{export_format}"
        )
        try:
            _export_format(
                export_format, export_path, armature, fbx_add_leaf_bones,
                fbx_primary_bone_axis, fbx_secondary_bone_axis
            )
        except Exception as e:
            print(f"Error exporting {export_format} file: {e}")
            raise

    # 5. Restore Original State
    bpy.ops.object.select_all(action='DESELECT')
    for marker in empties_parent.children:
        marker.matrix_world.translation = current_markers_position[marker.name]

    if restore_defaults_after_export:
        _restore_scene_defaults(
            armature=armature,
            data_parent_empty=data_parent_empty,
            mesh_object=mesh_object,
            armature_original_name=armature_original_name,
            current_bone_info=current_bone_info,
            rename_root_bone=rename_root_bone,
            bones_naming_convention=bones_naming_convention,
            rest_pose_type=rest_pose_type
        )


# --- Helper Functions ---


def _prepare_scene():
    """Deselect all objects and set frame to start."""
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.frame_set(bpy.context.scene.frame_start)


def _get_export_folder(destination_folder: str, add_subfolder: bool) -> str:
    """Determine the final export folder path."""
    if add_subfolder:
        export_folder = os.path.join(destination_folder, "3d_models")
        os.makedirs(export_folder, exist_ok=True)
        return export_folder
    return destination_folder


def _apply_bone_naming(armature: bpy.types.Object, naming_convention: str):
    """Rename bones according to the selected naming convention."""
    armature.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    for bone in armature.data.bones:
        if bone.name in bone_naming_mapping[naming_convention]:
            bone.name = bone_naming_mapping[naming_convention][bone.name]
    bpy.ops.object.mode_set(mode="OBJECT")
    armature.select_set(False)


def _export_format(
    export_format: str,
    export_path: str,
    armature: bpy.types.Object,
    fbx_add_leaf_bones: bool,
    fbx_primary_bone_axis: str,
    fbx_secondary_bone_axis: str
):
    """Route export to the appropriate format-specific function."""
    if export_format == "fbx":
        armature.select_set(True)
        child_objects = [
            obj for obj in bpy.data.objects if obj.parent == armature
        ]
        for child_object in child_objects:
            child_object.select_set(True)

        bpy.ops.export_scene.fbx(
            filepath=export_path,
            check_existing=True,
            use_selection=True,
            bake_anim=True,
            bake_anim_use_all_bones=True,
            bake_anim_use_nla_strips=False,
            bake_anim_use_all_actions=False,
            bake_anim_force_startend_keying=True,
            use_mesh_modifiers=True,
            add_leaf_bones=fbx_add_leaf_bones,
            bake_anim_step=1.0,
            bake_anim_simplify_factor=0.0,
            armature_nodetype='NULL',
            primary_bone_axis=fbx_primary_bone_axis,
            secondary_bone_axis=fbx_secondary_bone_axis,
        )
    elif export_format == "bvh":
        armature.select_set(True)
        bpy.context.view_layer.objects.active = armature

        bpy.ops.export_anim.bvh(
            filepath=export_path,
            check_existing=True,
            frame_start=bpy.context.scene.frame_start,
            frame_end=bpy.context.scene.frame_end,
            root_transform_only=False,
            global_scale=1.0,
        )
    elif export_format == "gltf":
        # TODO - Fix glTF export of animations - output appears broken
        bpy.ops.export_scene.gltf(
            filepath=export_path,
            check_existing=True,
            export_cameras=True,
            export_lights=True,
            use_visible=True,
        )
    else:
        raise ValueError(f"Unsupported file format: {export_format}")


def _restore_scene_defaults(
    armature: bpy.types.Object,
    data_parent_empty: bpy.types.Object,
    mesh_object: bpy.types.Object,
    armature_original_name: str,
    current_bone_info: dict,
    rename_root_bone: bool,
    bones_naming_convention: str,
    rest_pose_type: str
):
    """Restore armature, bones, mesh and names to their original state."""

    # --- EDIT MODE PASS ---
    bpy.ops.object.select_all(action='DESELECT')
    armature.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')

    # Restore bone names
    if bones_naming_convention != "default":
        inverse_mapping = {
            v: k for k, v in
            bone_naming_mapping[bones_naming_convention].items()
        }
        for bone in armature.data.bones:
            if bone.name in inverse_mapping:
                bone.name = inverse_mapping[bone.name]

    # Restore rest pose and rig-specific bone structure
    if rest_pose_type != "default":
        for bone in armature.data.edit_bones:
            if bone.name in current_bone_info:
                bone.head = current_bone_info[bone.name]['head_position']
                bone.tail = current_bone_info[bone.name]['tail_position']
                bone.roll = current_bone_info[bone.name]['roll']

        if rest_pose_type == 'metahuman':
            restore_metahuman_edit_mode(armature)
        elif rest_pose_type == 'daz_g8.1':
            restore_daz_g8_1_edit_mode(armature)

    bpy.ops.object.mode_set(mode='OBJECT')
    armature.select_set(False)

    # Re-align mesh based on restored pose
    if rest_pose_type != "default":
        align_and_parent_vertex_groups_to_armature(
            armature=armature,
            mesh_object=mesh_object,
            vertex_groups=_SKELLY_VERTEX_GROUPS
        )

    # --- POSE MODE PASS ---
    if rest_pose_type == 'metahuman':
        restore_metahuman_pose_mode(armature, data_parent_empty)
    elif rest_pose_type == 'daz_g8.1':
        restore_daz_g8_1_pose_mode(armature)

    # Restore original name
    if rename_root_bone:
        for obj in bpy.data.objects:
            if obj.type == "ARMATURE" and obj.name == "root":
                obj.name = armature_original_name

