from pathlib import Path
from typing import Dict

import bpy
from skelly_blender import PACKAGE_ROOT_PATH
from freemocap_blender_addon.models.animation.armatures.armature_definition import ArmatureDefinition


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
    skelly_meshes = load_skelly_fbx_files()

    # Iterate through the skelly bones dictionary and add the correspondent skelly mesh
    for bone in armature.pose.bones:
        print(f" Loading bone mesh for `{bone.name}` from: {mesh_path}")

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
    armature.select_set(True)
    # Set rig as active
    bpy.context.view_layer.objects.active = armature
    # Parent the mesh and the rig with automatic weights
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')


SKELLY_MESH_PREFIX = 'skelly_'
SKELLY_BONE_MESHES_PATH = Path(PACKAGE_ROOT_PATH) / "assets" / "skelly_bones" / "body" / "axial"


def load_skelly_fbx_files() -> Dict[str, bpy.types.Object]:
    meshes = {}
    for fbx_file_path in SKELLY_BONE_MESHES_PATH.glob("*.fbx"):
        bpy.ops.import_scene.fbx(filepath=str(fbx_file_path))
        mesh_name = fbx_file_path.stem
        meshes[mesh_name] = bpy.data.objects[mesh_name]

    return meshes
