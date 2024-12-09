import bpy
import os


def export_3d_model(
    rig: bpy.types.Armature,
    extensions: list = ['fbx'],# 'bvh'],
    recording_folder: str = '',
    rename_root_bone: bool=False,
) -> None:

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    armature_original_name = ''

    # Select the rig                
    rig.select_set(True)

    # Select the meshes parented to the armature
    child_objects = [obj for obj in bpy.data.objects if obj.parent == rig]
    for child_object in child_objects:
        child_object.select_set(True)

    # TODO - JSM - Do we need this?
    if rename_root_bone:
        # Save the original rig name to restore it after the export
        armature_original_name = rig.name
        # Rename the rig if its name is different from root
        if rig.name != "root":
            rig.name = "root"

    # # Select the armature.
    # for rig in bpy.data.objects:
    #     if rig.type == "ARMATURE":
    #         # Rename the root bone if rename_root_bone is True
    #         if rename_root_bone:
    #             # Save the original rig name to restore it after the export
    #             armature_original_name = rig.name
    #             # Rename the rig if its name is different from root
    #             if rig.name != "root":
    #                 rig.name = "root"
    #         break

    # Ensure the folder '3D_model' exists within the recording folder
    export_folder = os.path.join(recording_folder, "3D_model")
    os.makedirs(export_folder, exist_ok=True)

    # Export the file extensions
    for extension in extensions:

        # Set the export file name based on the recording folder name
        export_file_name = os.path.basename(recording_folder) + f".{extension}"
        export_path = os.path.join(export_folder, export_file_name)

        if extension == "fbx":
            bpy.ops.export_scene.fbx(
                filepath=export_path,
                check_existing=True,
                use_selection=True,
                bake_anim=True,
                bake_anim_use_all_bones=True,
                bake_anim_use_nla_strips=False,
                bake_anim_use_all_actions=False,
                bake_anim_force_startend_keying=True,
                add_leaf_bones=True,
            )

        elif extension == "bvh":
            bpy.ops.export_anim.bvh(
                filepath=export_path,
                check_existing=True,
                frame_start=bpy.context.scene.frame_start,
                frame_end=bpy.context.scene.frame_end,
                root_transform_only=False,
                global_scale=1.0,
                bone_correction_matrix=None,
            )
        else:
            raise ValueError(f"Unsupported file extension: {extension}")

    # Restore the name of the rig object
    if rename_root_bone:
        for rig in bpy.data.objects:
            if rig.type == "ARMATURE":
                # Restore the original rig name
                rig.name = armature_original_name
