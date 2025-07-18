import bpy
from mathutils import Vector, Euler

from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.helpers.mesh_utilities import get_bone_info
from ajc27_freemocap_blender_addon.core_functions.export_3d_model.helpers.rest_pose_types import rest_pose_type_rotations

def set_armature_rest_pose(
    data_parent_empty: bpy.types.Object,
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

            # If the bone is part of the palm, move its head to its parent
            # as it is not connected and didn't move with its parent rotation
            if 'palm' in bone.name or 'thumb.carpal' in bone.name:
                bone.head = bone.parent.head

            # If the armature is a metahuman, move the metacarpals using the offset info
            # if rest_pose_type == 'metahuman' and False:
            #     if bone.name in ['palm.01.L', 'palm.02.L', 'palm.03.L', 'palm.04.L']:
            #         print("Bone head position:", bone.head)
            #         print("Bone tail position:", bone_info[bone.name]['tail_position'])
            #         print("Bone length:", bone_info[bone.name]['length'])
            #         # Get the offset distance from the hand bone head
            #         offset_distance = rest_pose_rotations[bone.name]['position_offset']['wrist_newbonehead_to_wrist_mcp_ratio'] * bone_info[bone.name]['length']
            #         # Create the offset vector
            #         offset_vector = Vector([0, 0, offset_distance])
            #         # Get the rotation matrix
            #         rotation_matrix = Euler(
            #             Vector(rest_pose_rotations[bone.name]['position_offset']['rotation']),
            #                 'XYZ',
            #             ).to_matrix()
            #         # Rotate the offset vector
            #         bone.head = (
            #             bone.parent.head
            #             + rotation_matrix @ offset_vector
            #         )
            #         # Update the bone length
            #         bone_info[bone.name]['length'] = rest_pose_rotations[bone.name]['position_offset']['newbonehead_mcp_to_wrist_mcp_ratio'] * bone_info[bone.name]['length']
            #         print("Bone head position:", bone.head)
            #         print("Bone tail position:", bone_info[bone.name]['tail_position'])
            #         print("Bone length:", bone_info[bone.name]['length'])

            bone_vector = Vector(
                [0, 0, bone_info[bone.name]['length']]
            )

            # Get the rotation matrix
            rotation_matrix = Euler(
                Vector(rest_pose_rotations[bone.name]['rotation']),
                'XYZ',
            ).to_matrix()

            # Rotate the bone vector
            bone.tail = (
                bone.head
                + rotation_matrix @ bone_vector
            )

            # Assign the roll to the bone
            bone.roll = rest_pose_rotations[bone.name]['roll']

    # In case the rest pose type is metahuman, parent the thigh bones to the pelvis
    # and parent the thumb.01 bones to the hand
    if rest_pose_type == 'metahuman':
        for bone in armature.data.edit_bones:
            if 'thigh' in bone.name:
                bone.use_connect = False
                bone.parent = armature.data.edit_bones['pelvis']
            # if 'thumb.01.L' in bone.name:
            #     bone.use_connect = False
            #     bone.parent = armature.data.edit_bones['hand.L']
            #     bone.use_inherit_rotation = False

            #     # Get the thumb cmc marker
            #     thumb_cmc = [
            #         marker for marker in data_parent_empty.children_recursive
            #         if 'left_hand_thumb_cmc' in marker.name
            #     ][0]
            #     bone_location_constraint = armature.pose.bones[bone.name].constraints.new('COPY_LOCATION')
            #     bone_location_constraint.target = thumb_cmc
            #     armature.pose.bones[bone.name].constraints.move(1, 0)

    # Exit Edit Mode
    bpy.ops.object.mode_set(mode='OBJECT')        
