import bpy
from mathutils import Vector, Euler

from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.helpers.mesh_utilities import get_bone_info
from ajc27_freemocap_blender_addon.core_functions.export_3d_model.helpers.rest_pose_types import rest_pose_type_rotations

def set_armature_rest_pose(
    armature: bpy.types.Armature,
    rest_pose_type: str,
):
    print("Setting armature rest pose...")
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Select the armature
    armature.select_set(True)

    # Get the bone info (postions and lengths)
    bone_info = get_bone_info(armature)

    rest_pose_rotations = rest_pose_type_rotations[rest_pose_type]

    # Enter Edit Mode
    bpy.ops.object.mode_set(mode='EDIT')

    # Set the rest pose rotations
    for bone in armature.data.edit_bones:
        if bone.name in rest_pose_rotations:
            print(bone.name, bone_info[bone.name]['length'])

            # If the bone is part of the palm, move its head to its parent
            # as it is not connected and didn't move with its parent rotation
            if 'palm' in bone.name or 'thumb.carpal' in bone.name:
                bone.head = bone.parent.head

            bone_vector = Vector(
                [0, 0, bone_info[bone.name]['length']]
            )

            # Get the rotation matrix
            rotation_matrix = Euler(
                Vector(rest_pose_rotations[bone.name]['rotation']),
                'XYZ',
            ).to_matrix()

            # Rotate the bone vector
            # rotated_bone_vector = rotation_matrix @ bone_vector
            bone.tail = (
                bone.head
                + rotation_matrix @ bone_vector
            )

            # Assign the roll to the bone
            bone.roll = rest_pose_rotations[bone.name]['roll']

    # In case the rest pose type is metahuman, parent the thigh bones to the pelvis
    if rest_pose_type == 'metahuman':
        for bone in armature.data.edit_bones:
            if 'thigh' in bone.name:
                bone.use_connect = False
                bone.parent = armature.data.edit_bones['pelvis']

    # Exit Edit Mode
    bpy.ops.object.mode_set(mode='OBJECT')

        
