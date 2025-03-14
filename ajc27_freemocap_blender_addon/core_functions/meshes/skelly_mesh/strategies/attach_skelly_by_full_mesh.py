from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.skelly_mesh_paths import SKELLY_MESH_PATH

import bpy
def attach_skelly_complete_mesh(
    rig: bpy.types.Object,
    body_dimensions: dict[str, float],
    skelly_mesh_path: str = SKELLY_MESH_PATH
) -> None:

    try:
        # Get the script filepath
        # Import the skelly mesh

        # skelly_mesh_path = file_path.parent.parent.parent /"assets"/"skelly_lowpoly_mesh.fbx"
        if not Path(skelly_mesh_path).is_file():
            raise FileNotFoundError(f"Could not find skelly mesh at {skelly_mesh_path}")
        bpy.ops.import_scene.fbx(filepath=str(skelly_mesh_path))

    except Exception as e:
        print(f"Error while importing skelly mesh: {e}")
        print(traceback.format_exc())

    # Deselect all objects
    for object in bpy.data.objects:
        object.select_set(False)

    # Select the rig
    rig.select_set(True)
    bpy.context.view_layer.objects.active = rig

    # Change to edit mode
    bpy.ops.object.mode_set(mode='EDIT')

    # Get reference to the neck bone
    neck = rig.data.edit_bones['neck']

    # Change to object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Get the skelly mesh
    skelly_mesh = bpy.data.objects['Skelly_LowPoly_Mesh']

    # Get the neck bone tail position and save it as the head position
    head_location = (neck.tail[0], neck.tail[1], neck.tail[2])
    # Set the location of the skelly mesh
    skelly_mesh.location = head_location

    # Get the body mesh z dimension
    raw_body_mesh_wingspan_width = skelly_mesh.dimensions.x
    raw_body_mesh_toe_to_heel_depth = skelly_mesh.dimensions.y
    raw_body_mesh_height = skelly_mesh.dimensions.z

    # Calculate the proportion between the rig and the mesh
    rig_to_body_mesh_height_ratio =  body_dimensions['total_height'] / raw_body_mesh_height
    rig_to_body_mesh_wingspan_ratio =   body_dimensions['total_wingspan'] /raw_body_mesh_wingspan_width
    rig_to_body_mesh_toe_to_toe_ratio = body_dimensions['mean_foot_length'] /  raw_body_mesh_toe_to_heel_depth

    # Scale the mesh by the rig and body_mesh proportions multiplied by a scale factor
    skelly_mesh.scale = (rig_to_body_mesh_wingspan_ratio,
                            rig_to_body_mesh_toe_to_toe_ratio,
                            rig_to_body_mesh_height_ratio)

    # Set rig as active
    bpy.context.view_layer.objects.active = skelly_mesh

    # Select the skelly_mesh
    skelly_mesh.select_set(True)

    # Apply transformations to the mesh
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # Change skelly mesh origin to (0, 0, 0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    # Parent the skelly_mesh with the rig
    # Select the rig
    rig.select_set(True)
    # Set rig as active
    bpy.context.view_layer.objects.active = rig
    # Parent the body_mesh and the rig with automatic weights
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')

    # Rename the skelly mesh to fmc_mesh
    skelly_mesh.name = 'skelly_mesh'
