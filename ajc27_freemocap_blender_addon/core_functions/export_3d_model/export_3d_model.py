import bpy
import os

from ajc27_freemocap_blender_addon.core_functions.export_3d_model.helpers.set_armature_pose_by_markers import set_armature_pose_by_markers
from ajc27_freemocap_blender_addon.core_functions.export_3d_model.helpers.set_armature_rest_pose import set_armature_rest_pose
from ajc27_freemocap_blender_addon.core_functions.export_3d_model.helpers.bone_naming_mapping import bone_naming_mapping
from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.helpers.mesh_utilities import get_bone_info
from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.strategies.attach_skelly_by_vertex_groups import align_and_parent_vertex_groups_to_armature
from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.helpers.skelly_vertex_groups import (
    _SKELLY_VERTEX_GROUPS,
)


def export_3d_model(
        data_parent_empty: bpy.types.Object,
        armature: bpy.types.Armature,
        formats: list = ['fbx', 'bvh'],  # , 'gltf'],
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
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Set the frame to the scene start frame
    bpy.context.scene.frame_set(bpy.context.scene.frame_start)

    armature_original_name = ''

    # TODO - JSM - Do we need this?
    if rename_root_bone:
        # Save the original armature name to restore it after the export
        armature_original_name = armature.name
        # Rename the armature if its name is different from root
        if armature.name != "root":
            armature.name = "root"

    if add_subfolder:
        # Ensure the folder '3D_model' exists within the recording folder
        export_folder = os.path.join(destination_folder, "3d_models")
        os.makedirs(export_folder, exist_ok=True)
    else:
        export_folder = destination_folder

    # Get references to the mesh object
    mesh_object = [obj for obj in data_parent_empty.children_recursive if 'skelly_mesh' in obj.name][0]

    # Change the rest pose if its type is different than default
    if rest_pose_type != 'default':
        # Save the current rest pose with bone_info to restore it after the export
        current_bone_info = get_bone_info(armature)
        # Set the export rest pose
        set_armature_rest_pose(
            data_parent_empty=data_parent_empty,
            armature=armature,
            rest_pose_type=rest_pose_type
        )
        # Align and parent the mesh to the armature
        align_and_parent_vertex_groups_to_armature(
            armature=armature,
            mesh_object=mesh_object,
            vertex_groups=_SKELLY_VERTEX_GROUPS
        )

    # Get references to the empties_parent object
    empties_parent = [obj for obj in data_parent_empty.children if 'empties_parent' in obj.name][0]

    # Get the current frame action position of the markers and save it in a dictionary
    current_markers_position = {}
    for marker in empties_parent.children:
        current_markers_position[marker.name] = marker.matrix_world.translation.copy()

    # Set the markers position in frame 0 equal to the expected armature rest pose
    # This is because the exported fbx armature gets its rest pose as the
    # pose the armature has in the current frame before the export
    # Might be a change in the internal export function.
    set_armature_pose_by_markers(
        data_parent_empty=data_parent_empty,
        armature=armature
    )

    # Change the name of the bones according to the selected naming convention
    if bones_naming_convention != "default":
        armature.select_set(True)
        # Set Edit Mode
        bpy.ops.object.mode_set(mode="EDIT")

        for bone in armature.data.bones:
            if bone.name in bone_naming_mapping[bones_naming_convention]:
                bone.name = bone_naming_mapping[bones_naming_convention][bone.name]

        # Set Object Mode
        bpy.ops.object.mode_set(mode="OBJECT")
        armature.select_set(False)

    # Export the file formats
    for format in formats:
        
        # Set the export file name based on the recording folder name
        export_file_name = data_parent_empty.name.removesuffix("_origin") + f".{format}"
        export_path = os.path.join(export_folder, export_file_name)
        try:
            if format == "fbx":
                # Select the armature
                armature.select_set(True)

                # Select the meshes parented to the armature
                child_objects = [obj for obj in bpy.data.objects if obj.parent == armature]
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

            elif format == "bvh":
                armature.select_set(True)
                # set armature as active object
                bpy.context.view_layer.objects.active = armature

                bpy.ops.export_anim.bvh(
                    filepath=export_path,
                    check_existing=True,
                    frame_start=bpy.context.scene.frame_start,
                    frame_end=bpy.context.scene.frame_end,
                    root_transform_only=False,
                    global_scale=1.0,
                )

            elif format == "gltf":
                # TODO - Fix glTF export of animations - output appears broken
                bpy.ops.export_scene.gltf(
                    filepath=export_path,
                    check_existing=True,
                    export_cameras=True,
                    export_lights=True,
                    use_visible=True,
                )
            else:
                raise ValueError(f"Unsupported file format: {format}")
        except Exception as e:
            print(f"Error exporting {format} file: {e}")
            raise

    bpy.ops.object.select_all(action='DESELECT')

    # Restore (keyframe insert) the position of the markers in the start frame
    for marker in empties_parent.children:
        marker.matrix_world.translation = current_markers_position[marker.name]
        # Insert keyframe in the start frame
        marker.keyframe_insert(data_path="location", frame=bpy.context.scene.frame_start)


    if restore_defaults_after_export:
        # Restore the name of the bones 
        if bones_naming_convention != "default":
            armature.select_set(True)
            
            # Get the inverse mapping of the bone_naming_mapping
            inverse_bone_naming_mapping = {v: k for k, v in bone_naming_mapping[bones_naming_convention].items()}

            # Set Edit Mode
            bpy.ops.object.mode_set(mode="EDIT")

            for bone in armature.data.bones:
                if bone.name in inverse_bone_naming_mapping:
                    bone.name = inverse_bone_naming_mapping[bone.name]

            # Set Object Mode
            bpy.ops.object.mode_set(mode="OBJECT")
            armature.select_set(False)

        # Restore the rest pose of the armature if it was changed
        if rest_pose_type != "default":
            # Deselect all objects
            bpy.ops.object.select_all(action='DESELECT')
            # Select the armature
            armature.select_set(True)

            # Enter Edit Mode
            bpy.ops.object.mode_set(mode='EDIT')

            # Set the rest pose rotations
            for bone in armature.data.edit_bones:
                if bone.name in current_bone_info:
                    bone.head = current_bone_info[bone.name]['head_position']
                    bone.tail = current_bone_info[bone.name]['tail_position']
                    bone.roll = current_bone_info[bone.name]['roll']

            # Set Object Mode
            bpy.ops.object.mode_set(mode='OBJECT')
            armature.select_set(False)

            # Align and parent the mesh to the armature
            align_and_parent_vertex_groups_to_armature(
                armature=armature,
                mesh_object=mesh_object,
                vertex_groups=_SKELLY_VERTEX_GROUPS
            )

        # In case the rest pose type is metahuman or daz_g8.1, reparent the thigh bones to the pelvis.R and pelvis.L
        if rest_pose_type in ('metahuman', 'daz_g8.1'):
            # Select the armature
            armature.select_set(True)

            # Enter Edit Mode
            bpy.ops.object.mode_set(mode='EDIT')

            for bone in armature.data.edit_bones:
                if 'thigh' in bone.name:
                    if 'thigh.R' in bone.name:
                        bone.parent = armature.data.edit_bones['pelvis.R']
                    elif 'thigh.L' in bone.name:
                        bone.parent = armature.data.edit_bones['pelvis.L']
                    bone.use_connect = True

            # Set Object Mode
            bpy.ops.object.mode_set(mode='OBJECT')
            armature.select_set(False)

        # Recreate the thumb.carpal bones if the rest pose type is metahuman
        if rest_pose_type in ('metahuman', 'daz_g8.1'):
            # Select the armature
            armature.select_set(True)

            # Enter Edit Mode
            bpy.ops.object.mode_set(mode='EDIT')

            for side in ['.L', '.R']:
                if 'thumb.carpal' + side not in armature.data.edit_bones:
                    new_bone = armature.data.edit_bones.new(name='thumb.carpal' + side)
                    new_bone.head = armature.data.edit_bones['hand' + side].head.copy()
                    new_bone.tail = armature.data.edit_bones['thumb.01' + side].head.copy()
                    new_bone.roll = 0.0
                    new_bone.parent = armature.data.edit_bones['hand' + side]
                    new_bone.use_connect = False

            # Set Object Mode
            bpy.ops.object.mode_set(mode='OBJECT')
            armature.select_set(False)

        if rest_pose_type == 'metahuman':
            # Restore the hand bone connstraints target markers
            # TODO: Delete this code if the default target markers are not hand_middle and hand_thumb_cmc
            for side in ['left', 'right']:
                hand_bone = armature.pose.bones['hand' + '.' + side[0].upper()]

                # Get the hand_middle
                hand_middle = [
                    marker for marker in data_parent_empty.children_recursive
                    if side + '_hand_middle' == marker.name or side + '_hand_middle.' in marker.name # Consider suffixes like .001
                ][0]

                # Get the hand_thumb_cmc
                hand_thumb_cmc = [
                    marker for marker in data_parent_empty.children_recursive
                    if side + '_hand_thumb_cmc' in marker.name
                ][0]

                hand_bone.constraints['Damped Track'].target = hand_middle
                hand_bone.constraints['Locked Track'].target = hand_thumb_cmc

        if rest_pose_type == 'daz_g8.1':
            # Remove the DazG8.1_Face_Correction constraint if it exists
            if "DazG8.1_Face_Correction" in armature.pose.bones["face"].constraints:
                constraint = armature.pose.bones["face"].constraints["DazG8.1_Face_Correction"]
                armature.pose.bones["face"].constraints.remove(constraint)

            # Remove the DazG8.1_Pelvis_Correction constraint if it exists
            if "DazG8.1_Pelvis_Correction" in armature.pose.bones["pelvis"].constraints:
                constraint = armature.pose.bones["pelvis"].constraints["DazG8.1_Pelvis_Correction"]
                armature.pose.bones["pelvis"].constraints.remove(constraint)

            # Remove the DazG8.1_Spine_Correction constraint if it exists
            if "DazG8.1_Spine_Correction" in armature.pose.bones["spine"].constraints:
                constraint = armature.pose.bones["spine"].constraints["DazG8.1_Spine_Correction"]
                armature.pose.bones["spine"].constraints.remove(constraint)

            # Remove the DazG8.1_Forearm_Bend_Correction constraint if it exists
            for side in ['.L', '.R']:
                forearm_bone_name = 'forearm' + side
                if forearm_bone_name in armature.pose.bones:
                    forearm_bone = armature.pose.bones[forearm_bone_name]
                    if "DazG8.1_Forearm_Bend_Correction" in forearm_bone.constraints:
                        constraint = forearm_bone.constraints["DazG8.1_Forearm_Bend_Correction"]
                        forearm_bone.constraints.remove(constraint)

            # Remove the forearm twist bones if they were created
            armature.select_set(True)
            bpy.ops.object.mode_set(mode='EDIT')
            for side in ['.L', '.R']:
                twist_bone_name = 'forearm_twist' + side
                if twist_bone_name in armature.data.edit_bones:
                    bone = armature.data.edit_bones[twist_bone_name]
                    armature.data.edit_bones.remove(bone)

            # Set Object Mode
            bpy.ops.object.mode_set(mode='OBJECT')
            armature.select_set(False)

        # Restore the name of the armature object
        if rename_root_bone:
            for armature in bpy.data.objects:
                if armature.type == "ARMATURE":
                    # Restore the original armature name
                    armature.name = armature_original_name

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    return
