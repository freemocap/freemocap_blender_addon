import bpy

from skelly_blender.core.needs_bpy.armature_rig.armature.armature_definition_classes import ArmatureDefinition
from skelly_blender.core.needs_bpy.armature_rig.skelly_bone_meshes.skelly_bones_mesh_info import load_skelly_fbx_meshes

SKELLY_MESH_PREFIX = 'skelly_'


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
    skelly_meshes = load_skelly_fbx_meshes()

    # Iterate through the skelly bones dictionary and add the correspondent skelly mesh
    for host_armature_bone, bone_mesh_object in armature.pose.bones:
        print(f"Attaching mesh: `{bone_mesh_object.name}` to host armature bone: `{host_armature_bone}`")

        armature_bone = armature.data.edit_bones[host_armature_bone]
        # Get the rotation matrix
        rotation_matrix = armature_bone.rotation_matrix.to_3x3()

        # Move the Skelly part to the equivalent bone's head location
        # skelly_mesh.location = (bone.origin
        #                         + rotation_matrix @ Vector(SKELLY_BONE_MESHES[mesh].position_offset)
        #                         )

        # Rotate the part mesh with the rotation matrix
        # skelly_mesh.rotation_euler = rotation_matrix.to_euler('XYZ')
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
