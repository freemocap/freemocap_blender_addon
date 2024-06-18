from pathlib import Path

import bpy

from freemocap_blender_addon.core_functions.meshes.skelly_mesh.load_skelly_fbx_files import load_skelly_fbx_files
from freemocap_blender_addon.models.animation.armatures.armature_definition import ArmatureDefinition
from freemocap_blender_addon.models.animation.armatures.rest_pose.bone_pose_definition import ROOT_BONE_NAME
from freemocap_blender_addon.models.skeleton_model.body.segments.skull_segments import BlenderizedSkullSegments


def attach_skelly_bone_meshes(armature: bpy.types.Object,
                              armature_definition: ArmatureDefinition) -> None:
    bpy.ops.object.mode_set(mode='OBJECT')
    for thing in bpy.data.objects:
        thing.select_set(False)

    #  Set the rig as active object
    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature

    # Change to object mode
    bpy.ops.object.mode_set(mode='EDIT')
    axial_bone_names, skelly_meshes, skull_bone_names = load_skelly_fbx_files()

    # Iterate through the skelly bones dictionary and add the correspondent skelly mesh
    for bone in armature.pose.bones:
        if bone.name == ROOT_BONE_NAME:
            continue
        if bone.name in skull_bone_names:
            if bone.name == BlenderizedSkullSegments.NOSE.value:
                mesh_name = f"{SKELLY_MESH_PREFIX}skull"
            else:
                continue
        if not bone.name in axial_bone_names:
            continue
        else:
            mesh_name = f"{SKELLY_MESH_PREFIX}{bone.name}"
        mesh_path = SKELLY_BONE_MESHES_PATH / f"{mesh_name}.fbx"
        print(f" Loading bone mesh for `{bone.name}` from: {mesh_path}")

        # Import the skelly mesh
        if not Path(mesh_path).is_file():
            raise FileNotFoundError(f"Could not find skelly mesh at {mesh_path}")
        bpy.ops.import_scene.fbx(filepath=str(mesh_path))

        skelly_meshes.append(bpy.data.objects[mesh_name])

        # Get reference to the imported mesh
        skelly_mesh = bpy.data.objects[mesh_name]

        # Get the rotation matrix
        rotation_matrix = bone.rotation_matrix.to_3x3()

        # Move the Skelly part to the equivalent bone's head location
        # skelly_mesh.location = (bone.origin
        #                         + rotation_matrix @ Vector(SKELLY_BONE_MESHES[mesh].position_offset)
        #                         )

        # Rotate the part mesh with the rotation matrix
        skelly_mesh.rotation_euler = rotation_matrix.to_euler('XYZ')
        #
        # # Get the bone length
        # if SKELLY_BONE_MESHES[mesh].adjust_rotation:
        #     bone_length = (SKELLY_BONE_MESHES[mesh].bones_end - (SKELLY_BONE_MESHES[mesh].bones_origin + (
        #             rotation_matrix @ Vector(SKELLY_BONE_MESHES[mesh].position_offset)))).length
        # elif mesh == 'head':
        #     # bone_length = rig.data.edit_bones[bone_name_map[armature_name][SKELLY_BONES[mesh]['bones'][0]]].length
        #     bone_length = SKELLY_BONE_MESHES['spine'].bones_length / 3.123  # Head length to spine length ratio
        # else:
        #     bone_length = SKELLY_BONE_MESHES[mesh].bones_length
        #
        # # Get the mesh length
        # mesh_length = SKELLY_BONE_MESHES[mesh].mesh_length

        # # Resize the Skelly part to match the bone length
        # skelly_mesh.scale = (bone_length / mesh_length, bone_length / mesh_length, bone_length / mesh_length)

        # Apply the transformations to the Skelly part
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # Rename the first mesh to skelly_mesh
    skelly_meshes[0].name = "skelly_mesh"

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Select all body meshes
    for skelly_mesh in skelly_meshes:
        skelly_mesh.select_set(True)

    # Set skelly_mesh as active
    bpy.context.view_layer.objects.active = skelly_meshes[0]

    # Join the body meshes
    bpy.ops.object.join()

    # Select the rig
    rig.select_set(True)
    # Set rig as active
    bpy.context.view_layer.objects.active = rig
    # Parent the mesh and the rig with automatic weights
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
