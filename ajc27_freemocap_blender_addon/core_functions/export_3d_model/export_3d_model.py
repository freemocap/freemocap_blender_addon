import bpy
import os

from ajc27_freemocap_blender_addon.core_functions.export_3d_model.helpers.set_armature_pose_by_markers import set_armature_pose_by_markers
from ajc27_freemocap_blender_addon.core_functions.export_3d_model.helpers.set_armature_rest_pose import set_armature_rest_pose
from ajc27_freemocap_blender_addon.core_functions.export_3d_model.helpers.bone_naming_mapping import bone_naming_mapping


def export_3d_model(
        data_parent_empty: bpy.types.Object,
        armature: bpy.types.Armature,
        formats: list = ['fbx', 'bvh'],  # , 'gltf'],
        destination_folder: str = '',
        add_subfolder: bool = False,
        rename_root_bone: bool = False,
        bones_naming_convention: str = 'default',
        rest_pose_type: str = 'default',
        add_leaf_bones: bool = True,
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

    # Change the rest pose if its type is different than default
    if rest_pose_type != 'default':
        set_armature_rest_pose(
            armature=armature,
            rest_pose_type=rest_pose_type
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

    if bones_naming_convention != "default":
        armature.select_set(True)
        # Set Edit Mode
        bpy.ops.object.mode_set(mode="EDIT")
        print("Armature name: " + armature.name)

        for bone in armature.data.bones:
            if bone.name in bone_naming_mapping[bones_naming_convention]:
                bone.name = bone_naming_mapping[bones_naming_convention][bone.name]

        # Set Object Mode
        bpy.ops.object.mode_set(mode="OBJECT")
        armature.select_set(False)

    # Export the file formats
    for format in formats:
        
        # Set the export file name based on the recording folder name
        export_file_name = armature.name + f".{format}"
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
                    add_leaf_bones=add_leaf_bones,
                    bake_anim_step=1.0,
                    bake_anim_simplify_factor=0.0,
                    armature_nodetype='NULL',
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

    # Restore the name of the bones 
    if bones_naming_convention != "default":
        armature.select_set(True)
        
        # Get the inverse mapping of the bone_naming_mapping
        inverse_bone_naming_mapping = {v: k for k, v in bone_naming_mapping[bones_naming_convention].items()}

        # Set Edit Mode
        bpy.ops.object.mode_set(mode="EDIT")
        print("Armature name: " + armature.name)

        for bone in armature.data.bones:
            if bone.name in inverse_bone_naming_mapping:
                bone.name = inverse_bone_naming_mapping[bone.name]

        # Set Object Mode
        bpy.ops.object.mode_set(mode="OBJECT")
        armature.select_set(False)

    # Restore the name of the armature object
    if rename_root_bone:
        for armature in bpy.data.objects:
            if armature.type == "ARMATURE":
                # Restore the original armature name
                armature.name = armature_original_name


    return


