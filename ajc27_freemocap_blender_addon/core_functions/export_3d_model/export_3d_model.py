import bpy
import os


def export_3d_model(
        armature: bpy.types.Armature,
        formats: list = ['fbx', 'bvh'],  # , 'gltf'],
        destination_folder: str = '',
        add_subfolder: bool = False,
        rename_root_bone: bool = False,
        add_leaf_bones: bool = True,
) -> None:
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

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

    # Export the file formats
    for format in formats:
        bpy.ops.object.select_all(action='DESELECT')
        # set object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Set the export file name based on the recording folder name
        # export_file_name = os.path.basename(destination_folder) + f".{format}"
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
                    add_leaf_bones=add_leaf_bones,
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
    # Restore the name of the armature object
    if rename_root_bone:
        for armature in bpy.data.objects:
            if armature.type == "ARMATURE":
                # Restore the original armature name
                armature.name = armature_original_name
